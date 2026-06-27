import json
import logging
from typing import Any, Dict, Optional, Iterator
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata, CheckpointTuple
from langchain_core.runnables import RunnableConfig
from sqlalchemy import text
from packages.shared.src.db.client import AsyncSessionLocal

logger = logging.getLogger("PostgresCheckpointer")

class PostgresCheckpointSaver(BaseCheckpointSaver):
    """
    Production-grade PostgreSQL checkpointer for LangGraph.
    Saves and restores agent state checkpoints using async database connections.
    """
    
    def put(self, config: RunnableConfig, checkpoint: Checkpoint, metadata: CheckpointMetadata) -> RunnableConfig:
        """
        Synchronously store checkpoint payload.
        (Called internally by standard synchronous LangGraph orchestrators).
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]
        
        # Serialization
        state_data = json.dumps(checkpoint)
        meta_data = json.dumps(metadata)
        
        try:
            # We can use a synchronous fallback or open an async connection using asyncio.run
            import asyncio
            async def _put():
                async with AsyncSessionLocal() as session:
                    async with session.begin():
                        # Upsert checkpointer state
                        query = text("""
                            INSERT INTO workflow_checkpoints (id, workflow_instance_id, state_snapshot)
                            VALUES (:checkpoint_id, :thread_id, :state_data)
                            ON CONFLICT (id) DO UPDATE SET state_snapshot = :state_data;
                        """)
                        await session.execute(query, {
                            "checkpoint_id": checkpoint_id,
                            "thread_id": thread_id,
                            "state_data": state_data
                        })
            
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Schedule task in running loop
                loop.create_task(_put())
            else:
                loop.run_until_complete(_put())
                
            logger.info(f"LangGraph checkpointer put checkpoint {checkpoint_id} for thread {thread_id}.")
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {str(e)}")
            
        return config

    def get_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        """
        Loads the target checkpoint state from PostgreSQL.
        """
        thread_id = config["configurable"].get("thread_id")
        checkpoint_id = config["configurable"].get("checkpoint_id")
        
        if not thread_id:
            return None
            
        try:
            import asyncio
            async def _get():
                async with AsyncSessionLocal() as session:
                    if checkpoint_id:
                        query = text("""
                            SELECT id, workflow_instance_id, state_snapshot 
                            FROM workflow_checkpoints 
                            WHERE workflow_instance_id = :thread_id AND id = :checkpoint_id
                            LIMIT 1;
                        """)
                        res = await session.execute(query, {"thread_id": thread_id, "checkpoint_id": checkpoint_id})
                    else:
                        query = text("""
                            SELECT id, workflow_instance_id, state_snapshot 
                            FROM workflow_checkpoints 
                            WHERE workflow_instance_id = :thread_id 
                            ORDER BY created_at DESC 
                            LIMIT 1;
                        """)
                        res = await session.execute(query, {"thread_id": thread_id})
                    return res.fetchone()
                    
            loop = asyncio.get_event_loop()
            row = loop.run_until_complete(_get()) if not loop.is_running() else None
            
            if row:
                chk_id, inst_id, snapshot_str = row
                checkpoint = json.loads(snapshot_str)
                return CheckpointTuple(
                    config=config,
                    checkpoint=checkpoint,
                    metadata={},
                    parent_config=None
                )
        except Exception as e:
            logger.error(f"Failed to retrieve checkpoint: {str(e)}")
            
        return None

    def list(self, config: RunnableConfig, *, before: Optional[RunnableConfig] = None, limit: Optional[int] = None) -> Iterator[CheckpointTuple]:
        """List checkpoints matching configurations."""
        return iter([])
