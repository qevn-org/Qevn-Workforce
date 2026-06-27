from typing import Dict, Any, Type, Optional
from packages.tools.src.base import BaseTool, ToolException
from packages.tools.src.integrations.gmail import GmailTool
from packages.tools.src.integrations.hubspot import HubSpotTool
from packages.tools.src.integrations.slack import SlackTool
from packages.tools.src.integrations.twilio import TwilioTool
from packages.tools.src.integrations.calendar import CalendarTool


class ToolRegistry:
    """
    Registry of all available SaaS and functional tools in QEVN Workforce.
    Loads and provides tool instances bound to employee integration credentials.
    """

    _registry: Dict[str, Type[BaseTool]] = {
        "GmailTool": GmailTool,
        "HubSpotTool": HubSpotTool,
        "SlackTool": SlackTool,
        "TwilioTool": TwilioTool,
        "CalendarTool": CalendarTool,
    }

    @classmethod
    def get_tool(
        cls, tool_name: str, credentials: Optional[Dict[str, Any]] = None
    ) -> BaseTool:
        """
        Instantiates and retrieves the requested tool, bound to credentials.
        """
        tool_class = cls._registry.get(tool_name)
        if not tool_class:
            raise ToolException(
                f"Tool {tool_name} is not registered in the Tool Registry."
            )
        return tool_class(credentials=credentials)

    @classmethod
    def list_available_tools(cls) -> Dict[str, str]:
        """
        Lists all registered tools and their baseline definitions.
        """
        return {name: clazz.description for name, clazz in cls._registry.items()}
