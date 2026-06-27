-- Seed file for AI SDR Employee configurations

-- 1. Seed Capabilities
INSERT INTO capabilities (id, name, description, version, supported_actions, required_tools, created_at)
VALUES 
(
    'sdr_research_v1', 
    'SDR Prospect Research', 
    'Enriches domain and contact info for target ICP criteria.', 
    '1.0.0', 
    '["search_company", "search_contact"]'::jsonb, 
    '[]'::jsonb, 
    CURRENT_TIMESTAMP
),
(
    'sdr_outreach_v1', 
    'SDR Outreach & CRM Sync', 
    'Coordinates Gmail threading and qualifies leads into HubSpot.', 
    '1.0.0', 
    '["score_lead", "sync_hubspot", "dispatch_outreach"]'::jsonb, 
    '["GmailTool", "HubSpotTool"]'::jsonb, 
    CURRENT_TIMESTAMP
)
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    supported_actions = EXCLUDED.supported_actions,
    required_tools = EXCLUDED.required_tools;

-- 2. Seed Employee Template Configurations
INSERT INTO employees (id, organization_id, name, description, role_title, department, system_prompt, working_hours, timezone, escalation_rules, approval_rules)
VALUES (
    'employee-sdr-001',
    '00000000-0000-0000-0000-000000000000', -- Default system org
    'Alex Outbound',
    'AI Outbound Sales Representative qualifying leads and booking meetings.',
    'Outbound SDR',
    'Sales',
    'You are a senior Outbound SDR. Qualify prospects and sync details to CRM.',
    '{"start": "09:00", "end": "17:00", "days": [1,2,3,4,5]}'::jsonb,
    'UTC',
    '{"on_error": "notify_slack"}'::jsonb,
    '{"require_approval_for": ["dispatch_outreach"]}'::jsonb
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    system_prompt = EXCLUDED.system_prompt,
    working_hours = EXCLUDED.working_hours,
    approval_rules = EXCLUDED.approval_rules;

-- 3. Seed Employee Capabilities Mapping
INSERT INTO employee_capabilities (id, employee_id, capability_id, config)
VALUES 
(
    uuid_generate_v4(),
    'employee-sdr-001',
    'sdr_research_v1',
    '{"search_depth": "deep"}'::jsonb
),
(
    uuid_generate_v4(),
    'employee-sdr-001',
    'sdr_outreach_v1',
    '{"crm_provider": "hubspot", "threading": true}'::jsonb
)
ON CONFLICT (employee_id, capability_id) DO NOTHING;
