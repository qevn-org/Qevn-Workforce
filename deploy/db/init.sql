-- SQL script to initialize QEVN Workforce Database Schema in Supabase / Postgres

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Organizations
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed default system organization
INSERT INTO organizations (id, name, slug)
VALUES ('00000000-0000-0000-0000-000000000000', 'System Default Organization', 'system-default-org')
ON CONFLICT (id) DO NOTHING;


-- Roles & Permissions
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    clerk_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role_id UUID REFERENCES roles(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI Employees
CREATE TABLE IF NOT EXISTS employees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    avatar_url TEXT,
    department VARCHAR(100),
    role_title VARCHAR(100),
    system_prompt TEXT NOT NULL,
    working_hours JSONB NOT NULL DEFAULT '{"start": "09:00", "end": "17:00", "days": [1, 2, 3, 4, 5]}'::jsonb,
    timezone VARCHAR(50) DEFAULT 'UTC',
    escalation_rules JSONB NOT NULL DEFAULT '{"on_error": "notify_slack"}'::jsonb,
    approval_rules JSONB NOT NULL DEFAULT '{"require_approval_for": []}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Capabilities Registry Inventory
CREATE TABLE IF NOT EXISTS capabilities (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(50) NOT NULL,
    supported_actions JSONB NOT NULL,
    required_tools JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Employee Capabilities
CREATE TABLE IF NOT EXISTS employee_capabilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    capability_id VARCHAR(100) NOT NULL REFERENCES capabilities(id) ON DELETE CASCADE,
    config JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (employee_id, capability_id)
);

-- Employee Tools
CREATE TABLE IF NOT EXISTS employee_tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    encrypted_credentials TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (employee_id, tool_name)
);

-- Conversations
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    title VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workflows
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    definition JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    current_state JSONB NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE
);

-- Tool Calls
CREATE TABLE IF NOT EXISTS tool_calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_run_id UUID REFERENCES workflow_runs(id) ON DELETE SET NULL,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    arguments JSONB NOT NULL,
    response TEXT,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    target_id UUID,
    ip_address VARCHAR(45),
    user_agent TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Billing
CREATE TABLE IF NOT EXISTS billing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR(255) UNIQUE,
    billing_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    status VARCHAR(50) NOT NULL,
    price_id VARCHAR(255) NOT NULL,
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Memories
CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID REFERENCES employees(id) ON DELETE CASCADE,
    memory_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    vector_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    action_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Capability Telemetry & Performance Metrics
CREATE TABLE IF NOT EXISTS capability_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_run_id UUID REFERENCES workflow_runs(id) ON DELETE CASCADE,
    capability_id VARCHAR(100) REFERENCES capabilities(id) ON DELETE SET NULL,
    latency_ms INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    llm_cost NUMERIC(10, 6),
    success BOOLEAN,
    hallucination_score REAL,
    human_override BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Skills Registry
CREATE TABLE IF NOT EXISTS skills (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workflow Instances & State Logging
CREATE TABLE IF NOT EXISTS workflow_instances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID REFERENCES employees(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    goal TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_checkpoints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_instance_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    capability_id VARCHAR(100) REFERENCES capabilities(id),
    inputs JSONB NOT NULL,
    outputs JSONB,
    state_snapshot JSONB NOT NULL,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Policy Rules & Decisions
CREATE TABLE IF NOT EXISTS policy_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    rule_name VARCHAR(100) NOT NULL,
    rule_type VARCHAR(50) NOT NULL,
    definition JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS policy_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_instance_id UUID REFERENCES workflow_instances(id) ON DELETE CASCADE,
    rule_id UUID REFERENCES policy_rules(id) ON DELETE SET NULL,
    action_attempted VARCHAR(255) NOT NULL,
    decision VARCHAR(50) NOT NULL,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Human Approval Requests
CREATE TABLE IF NOT EXISTS approvals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_instance_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    checkpoint_id UUID REFERENCES workflow_checkpoints(id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'requested',
    approver_id UUID REFERENCES users(id),
    escalated BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Evaluation & Performance Telemetry
CREATE TABLE IF NOT EXISTS evaluation_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_instance_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    latency_ms INTEGER NOT NULL,
    llm_cost NUMERIC(10, 6) NOT NULL,
    token_usage INTEGER NOT NULL,
    hallucination_score REAL,
    completion_score REAL,
    human_override_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- RLS Isolation Policies
ALTER TABLE workflow_instances ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_workflow ON workflow_instances
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

ALTER TABLE policy_rules ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_policies ON policy_rules
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

-- Marketplace Packages Catalog
CREATE TABLE IF NOT EXISTS packages (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    author VARCHAR(255) NOT NULL,
    license VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Version Releases
CREATE TABLE IF NOT EXISTS package_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_id VARCHAR(100) REFERENCES packages(id) ON DELETE CASCADE,
    version VARCHAR(50) NOT NULL,
    manifest JSONB NOT NULL,
    sha256_hash VARCHAR(64) NOT NULL,
    storage_path TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (package_id, version)
);

-- Dependencies Mapping
CREATE TABLE IF NOT EXISTS package_dependencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    package_version_id UUID REFERENCES package_versions(id) ON DELETE CASCADE,
    dependent_package_id VARCHAR(100) REFERENCES packages(id) ON DELETE CASCADE,
    version_constraint VARCHAR(50) NOT NULL
);

-- Tenant Package Installations
CREATE TABLE IF NOT EXISTS package_installations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    package_id VARCHAR(100) REFERENCES packages(id) ON DELETE CASCADE,
    installed_version VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (organization_id, package_id)
);

ALTER TABLE package_installations ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_packages ON package_installations
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

-- Indexing for multi-tenancy Performance
CREATE INDEX IF NOT EXISTS idx_users_org ON users(organization_id);
CREATE INDEX IF NOT EXISTS idx_employees_org ON employees(organization_id);
CREATE INDEX IF NOT EXISTS idx_conversations_org ON conversations(organization_id);
CREATE INDEX IF NOT EXISTS idx_tasks_org ON tasks(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_org ON audit_logs(organization_id);
CREATE INDEX IF NOT EXISTS idx_memories_employee ON memories(employee_id);

-- ==========================================
-- ENTERPRISE INTEGRATION HUB SCHEMAS
-- ==========================================

-- Centralized Integrations Catalogue
CREATE TABLE IF NOT EXISTS integration_connectors (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manifest JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workspace / Tenant Connector Installations
CREATE TABLE IF NOT EXISTS connector_installations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    connector_id VARCHAR(100) REFERENCES integration_connectors(id) ON DELETE CASCADE,
    config JSONB NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (organization_id, connector_id)
);

-- Central OAuth Credentials Store (AES-GCM encrypted values)
CREATE TABLE IF NOT EXISTS oauth_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    installation_id UUID REFERENCES connector_installations(id) ON DELETE CASCADE,
    account_identifier VARCHAR(255) NOT NULL,
    encrypted_access_token BYTEA NOT NULL,
    encrypted_refresh_token BYTEA,
    token_expiry TIMESTAMP WITH TIME ZONE,
    scopes TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Webhook Subscriptions mapping
CREATE TABLE IF NOT EXISTS webhook_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    installation_id UUID REFERENCES connector_installations(id) ON DELETE CASCADE,
    external_webhook_id VARCHAR(255),
    event_type VARCHAR(100) NOT NULL,
    secret_key VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Webhook Dead Letter Queue (DLQ)
CREATE TABLE IF NOT EXISTS webhook_dlq (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subscription_id UUID REFERENCES webhook_subscriptions(id) ON DELETE SET NULL,
    payload JSONB NOT NULL,
    headers JSONB NOT NULL,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Row-Level Security (RLS) Enablement & Tenant Isolation
ALTER TABLE connector_installations ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_connector_installations ON connector_installations
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

ALTER TABLE oauth_connections ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_oauth_connections ON oauth_connections
    FOR ALL USING (installation_id IN (
        SELECT id FROM connector_installations WHERE organization_id = CURRENT_SETTING('app.current_organization_id')::UUID
    ));

ALTER TABLE webhook_subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_webhook_subs ON webhook_subscriptions
    FOR ALL USING (installation_id IN (
        SELECT id FROM connector_installations WHERE organization_id = CURRENT_SETTING('app.current_organization_id')::UUID
    ));

ALTER TABLE webhook_dlq ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_webhook_dlq ON webhook_dlq
    FOR ALL USING (subscription_id IN (
        SELECT id FROM webhook_subscriptions WHERE installation_id IN (
            SELECT id FROM connector_installations WHERE organization_id = CURRENT_SETTING('app.current_organization_id')::UUID
        )
    ));

-- AI EVALUATION PLATFORM SCHEMAS
-- ==========================================

-- Prompt Versions
CREATE TABLE IF NOT EXISTS prompt_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    version VARCHAR(50) NOT NULL,
    prompt_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (employee_id, version)
);

-- Experiments (A/B testing, Shadow mode, Canaries)
CREATE TABLE IF NOT EXISTS experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    experiment_type VARCHAR(50) NOT NULL, -- 'ab_test', 'shadow', 'canary'
    champion_prompt_version_id UUID REFERENCES prompt_versions(id) ON DELETE SET NULL,
    challenger_prompt_version_id UUID REFERENCES prompt_versions(id) ON DELETE SET NULL,
    champion_model VARCHAR(100) NOT NULL DEFAULT 'claude-3-5-sonnet',
    challenger_model VARCHAR(100) NOT NULL,
    traffic_split REAL DEFAULT 0.5, -- fraction of traffic to challenger
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed', 'draft'
    winner VARCHAR(50), -- 'champion', 'challenger'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Benchmark Suites for Regression Testing
CREATE TABLE IF NOT EXISTS benchmark_suites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Benchmark Test Cases
CREATE TABLE IF NOT EXISTS benchmark_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    suite_id UUID NOT NULL REFERENCES benchmark_suites(id) ON DELETE CASCADE,
    input_goal TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    case_type VARCHAR(50) DEFAULT 'golden', -- 'golden', 'edge_case', 'failure_case', 'prompt_injection', 'policy_violation'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Benchmark Execution Runs
CREATE TABLE IF NOT EXISTS benchmark_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    suite_id UUID NOT NULL REFERENCES benchmark_suites(id) ON DELETE CASCADE,
    prompt_version_id UUID REFERENCES prompt_versions(id) ON DELETE SET NULL,
    model_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'running', -- 'running', 'completed', 'failed'
    score REAL DEFAULT 0.0, -- percentage of test cases passed (0.0 to 1.0)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Benchmark Case Results
CREATE TABLE IF NOT EXISTS benchmark_case_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID NOT NULL REFERENCES benchmark_runs(id) ON DELETE CASCADE,
    case_id UUID NOT NULL REFERENCES benchmark_cases(id) ON DELETE CASCADE,
    actual_output TEXT,
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    latency_ms INTEGER,
    cost NUMERIC(10, 6) DEFAULT 0.000000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Employee scorecards
CREATE TABLE IF NOT EXISTS employee_scorecards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    quality_score REAL DEFAULT 0.0,
    reliability_score REAL DEFAULT 0.0,
    business_score REAL DEFAULT 0.0,
    cost_efficiency_score REAL DEFAULT 0.0,
    safety_score REAL DEFAULT 0.0,
    overall_score REAL DEFAULT 0.0,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Human Feedback Collection
CREATE TABLE IF NOT EXISTS human_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_instance_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    rating VARCHAR(20) NOT NULL, -- 'thumbs_up', 'thumbs_down'
    correction TEXT,
    edit_history JSONB DEFAULT '[]'::jsonb,
    decision VARCHAR(50), -- 'approved', 'rejected', 'escalated'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- RLS Tenant Isolation Policies
ALTER TABLE prompt_versions ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_prompt_versions ON prompt_versions
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

ALTER TABLE experiments ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_experiments ON experiments
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

ALTER TABLE benchmark_suites ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_benchmark_suites ON benchmark_suites
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

ALTER TABLE benchmark_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_benchmark_runs ON benchmark_runs
    FOR ALL USING (suite_id IN (
        SELECT id FROM benchmark_suites WHERE organization_id = CURRENT_SETTING('app.current_organization_id')::UUID
    ));

ALTER TABLE benchmark_case_results ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_benchmark_case_results ON benchmark_case_results
    FOR ALL USING (run_id IN (
        SELECT id FROM benchmark_runs WHERE suite_id IN (
            SELECT id FROM benchmark_suites WHERE organization_id = CURRENT_SETTING('app.current_organization_id')::UUID
        )
    ));

ALTER TABLE employee_scorecards ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_employee_scorecards ON employee_scorecards
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);

ALTER TABLE human_feedback ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_human_feedback ON human_feedback
    FOR ALL USING (organization_id = CURRENT_SETTING('app.current_organization_id')::UUID);
