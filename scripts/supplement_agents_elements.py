#!/usr/bin/env python3
"""
Script to systematically add Element 4, 7, and 13 to F2-F9 agents.
Based on F1 pattern and SKILL.md 13-element framework.
"""

import re
from pathlib import Path

# Base path
AGENTS_DIR = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/plugins/开发组/agents")

# Agent definitions with custom content for Element 4 (Professional Domain)
AGENT_DOMAINS = {
    "F2": {
        "primary": "UI Component Library Architecture - Design Systems",
        "primary_bullets": [
            "shadcn/ui and Radix UI component patterns",
            "Accessibility standards and WCAG 2.1 AA compliance",
            "Component API design and TypeScript interfaces",
            "Performance optimization and bundle size management"
        ],
        "secondary": [
            "Tailwind CSS and CSS-in-JS styling systems",
            "Storybook documentation and visual regression testing",
            "React Hook patterns and custom hooks development",
            "Build tools optimization (Vite, Turbopack)"
        ],
        "standards": [
            "shadcn/ui design principles and component patterns",
            "WCAG 2.1 Level AA accessibility standards",
            "Atomic Design methodology (atoms → molecules → organisms)",
            "Component testing standards: 80%+ coverage, a11y compliance",
            "Chromatic visual regression testing protocols"
        ],
        "project_examples": [
            "餐饮组件库重构 (Restaurant Component Library Refactor)",
            "无障碍组件升级 (Accessibility Component Upgrade)",
            "Storybook文档系统建设 (Storybook Documentation System)"
        ]
    },
    "F3": {
        "primary": "Database Architecture & Data Modeling - PostgreSQL Ecosystems",
        "primary_bullets": [
            "Relational database design and normalization theory",
            "PostgreSQL advanced features and query optimization",
            "Prisma ORM and type-safe database access",
            "Database performance tuning and indexing strategies"
        ],
        "secondary": [
            "NoSQL databases (MongoDB, Redis) for specific use cases",
            "Database security and Row Level Security (RLS)",
            "Migration strategies and schema evolution",
            "Backup, recovery, and disaster preparedness"
        ],
        "standards": [
            "Database normalization forms: 1NF, 2NF, 3NF, BCNF",
            "PostgreSQL performance best practices and query plans",
            "Prisma schema conventions and migration workflows",
            "ACID transaction guarantees and isolation levels",
            "Database security standards: encryption at rest, RLS policies"
        ],
        "project_examples": [
            "餐饮管理系统数据库设计 (Restaurant Management DB Design)",
            "会员积分系统数据模型 (Membership Points Data Model)",
            "订单性能优化 (Order System Performance Optimization)"
        ]
    },
    "F4": {
        "primary": "API Architecture & Contract Design - RESTful/GraphQL/tRPC",
        "primary_bullets": [
            "RESTful API design principles and resource modeling",
            "GraphQL schema design and resolver optimization",
            "tRPC end-to-end type safety and procedure design",
            "API security, authentication, and authorization"
        ],
        "secondary": [
            "OpenAPI 3.0/Swagger documentation generation",
            "API versioning strategies and backward compatibility",
            "Rate limiting, throttling, and DDoS protection",
            "Third-party API integration patterns"
        ],
        "standards": [
            "RESTful API best practices: resource naming, HTTP methods, status codes",
            "GraphQL schema design patterns and N+1 problem resolution",
            "OpenAPI 3.0 specification compliance",
            "OAuth 2.0/JWT authentication standards",
            "API performance targets: P95 < 500ms, availability 99.9%"
        ],
        "project_examples": [
            "餐饮订单API系统设计 (Restaurant Order API Design)",
            "会员服务GraphQL迁移 (Member Service GraphQL Migration)",
            "第三方支付集成 (Third-Party Payment Integration)"
        ]
    },
    "F5": {
        "primary": "Backend System Architecture - Business Logic & Microservices",
        "primary_bullets": [
            "Business logic modeling and workflow orchestration",
            "Microservices architecture and service decomposition",
            "Distributed systems patterns and communication protocols",
            "Backend performance optimization and scalability"
        ],
        "secondary": [
            "Message queues (RabbitMQ, Kafka) for async processing",
            "Caching strategies (Redis) for performance",
            "Service mesh and API gateway patterns",
            "Event-driven architecture and CQRS patterns"
        ],
        "standards": [
            "12-Factor App methodology for cloud-native applications",
            "Microservices design patterns: SAGA, Circuit Breaker, Bulkhead",
            "Domain-Driven Design (DDD) principles for complex domains",
            "Backend testing standards: unit 80%+, integration, contract tests",
            "SLA targets: 99.9% availability, MTTR < 15 minutes"
        ],
        "project_examples": [
            "订单处理微服务架构 (Order Processing Microservices)",
            "库存管理业务逻辑重构 (Inventory Management Refactor)",
            "异步任务队列系统 (Async Task Queue System)"
        ]
    },
    "F6": {
        "primary": "AI Integration Architecture - Agent Orchestration & Prompt Engineering",
        "primary_bullets": [
            "Claude/OpenAI API integration patterns",
            "Prompt engineering techniques (few-shot, CoT, ReAct)",
            "Multi-agent systems design (Swarm, LangChain)",
            "RAG system architecture and vector databases"
        ],
        "secondary": [
            "MCP (Model Context Protocol) server development",
            "Token optimization and cost control strategies",
            "AI system observability and error handling",
            "Fine-tuning and model evaluation workflows"
        ],
        "standards": [
            "Anthropic prompt engineering best practices",
            "OpenAI API integration guidelines and rate limiting",
            "Multi-agent coordination patterns: hierarchical, peer-to-peer",
            "RAG evaluation metrics: retrieval precision, answer relevance",
            "AI system SLAs: latency P95 < 5s, accuracy > 85%"
        ],
        "project_examples": [
            "智能客服多智能体系统 (Intelligent Customer Service Multi-Agent)",
            "菜单分析RAG系统 (Menu Analysis RAG System)",
            "AI驱动的需求分析助手 (AI-Powered Requirements Analysis)"
        ]
    },
    "F7": {
        "primary": "Quality Assurance & Performance Engineering - Testing Strategies",
        "primary_bullets": [
            "Test strategy design (unit, integration, E2E)",
            "Performance testing and load testing methodologies",
            "Test automation framework architecture",
            "CI/CD pipeline integration and quality gates"
        ],
        "secondary": [
            "Security testing (OWASP ZAP, penetration testing)",
            "Accessibility testing (axe-core, Pa11y)",
            "Visual regression testing (Chromatic, Percy)",
            "Test data management and test environment setup"
        ],
        "standards": [
            "Testing pyramid: 70% unit, 20% integration, 10% E2E",
            "Code coverage standards: 80%+ for critical paths",
            "Performance benchmarks: load tests before major releases",
            "CI/CD quality gates: all tests pass, coverage thresholds met",
            "Accessibility standards: WCAG 2.1 AA compliance testing"
        ],
        "project_examples": [
            "订单系统性能测试方案 (Order System Performance Testing)",
            "自动化测试框架建设 (Automated Testing Framework)",
            "E2E测试覆盖率提升 (E2E Test Coverage Improvement)"
        ]
    },
    "F8": {
        "primary": "Version Control & Release Engineering - Git Workflows & CI/CD",
        "primary_bullets": [
            "Git workflow design (Git Flow, GitHub Flow, Trunk-Based)",
            "Code review processes and quality enforcement",
            "Semantic versioning and changelog management",
            "CI/CD pipeline architecture and deployment automation"
        ],
        "secondary": [
            "Branch protection rules and merge strategies",
            "Git hooks for quality gates (pre-commit, pre-push)",
            "Release tagging and artifact management",
            "Deployment rollback and hotfix procedures"
        ],
        "standards": [
            "Conventional Commits specification for commit messages",
            "Git Flow branching model for complex projects",
            "Semantic Versioning (SemVer) for version numbering",
            "Pull Request review checklist: code quality, tests, docs",
            "CI/CD standards: automated tests, linting, security scans"
        ],
        "project_examples": [
            "Git工作流规范制定 (Git Workflow Standards)",
            "CI/CD流水线优化 (CI/CD Pipeline Optimization)",
            "版本发布自动化系统 (Version Release Automation)"
        ]
    },
    "F9": {
        "primary": "Cloud Infrastructure & DevOps - Deployment Strategies & Monitoring",
        "primary_bullets": [
            "Container orchestration (Docker, Kubernetes)",
            "Cloud platform architecture (Vercel, AWS, Supabase)",
            "Infrastructure as Code (IaC) and configuration management",
            "Monitoring, observability, and incident response"
        ],
        "secondary": [
            "Blue-green and canary deployment strategies",
            "Service mesh and API gateway configuration",
            "Disaster recovery and backup strategies",
            "Cost optimization and resource management"
        ],
        "standards": [
            "12-Factor App principles for cloud-native deployments",
            "Kubernetes best practices: resource limits, health checks, rolling updates",
            "Monitoring standards: Prometheus metrics, Grafana dashboards, alerting rules",
            "SLO/SLA targets: 99.9% availability, MTTR < 15 minutes",
            "Security standards: container scanning, secrets management, network policies"
        ],
        "project_examples": [
            "Kubernetes集群部署方案 (Kubernetes Cluster Deployment)",
            "监控告警系统建设 (Monitoring & Alerting System)",
            "蓝绿部署流程优化 (Blue-Green Deployment Optimization)"
        ]
    }
}

def add_elements_to_agent(agent_id: str) -> None:
    """Add Element 4, 7, and 13 to an agent file."""
    file_path = None
    for path in AGENTS_DIR.glob(f"{agent_id}-*.md"):
        file_path = path
        break

    if not file_path:
        print(f"❌ Agent file not found for {agent_id}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if elements already exist
    if "## Professional Domain" in content:
        print(f"✅ {agent_id} already has Professional Domain")
        return

    domain = AGENT_DOMAINS[agent_id]

    # Construct Element 4 (Professional Domain)
    element4 = f"""
## Professional Domain

**Primary Domain**: {domain['primary']}
{chr(10).join(f"- {bullet}" for bullet in domain['primary_bullets'])}

**Secondary Domains**:
{chr(10).join(f"- {item}" for item in domain['secondary'])}

**Domain Standards**:
{chr(10).join(f"- {std}" for std in domain['standards'])}
"""

    # Find insertion point after "Your Core Identity" or similar sections
    patterns = [
        r"(## Your Core Identity.*?)(\n\n##)",
        r"(## Your Technical Stack.*?)(\n\n##)",
        r"(## Your Expertise.*?)(\n\n##)"
    ]

    inserted = False
    for pattern in patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, rf"\1{element4}\2", content, count=1, flags=re.DOTALL)
            inserted = True
            break

    if not inserted:
        # Fallback: insert after frontmatter and first section
        lines = content.split('\n')
        insert_idx = 20  # Approximate position
        content = '\n'.join(lines[:insert_idx] + [element4] + lines[insert_idx:])

    # Construct Element 7 (Skills & Tool Dependencies) - insert before "Collaboration" or similar
    element7 = f"""
## Task Mode

### Independent Mode (用户单独调用)
When called directly by the user:
1. Execute the assigned planning task
2. Produce outputs as specified
3. **Interactive Proposal**: Suggest next coordination steps

### Batch/Orchestrated Mode (批量任务/上级调度)
When called by FF-开发团队组长 or in multi-project batch:
1. Execute the assigned planning task
2. Auto-generate coordination plan
3. Return structured outputs to orchestrator without user confirmation

**Mode Detection**: Automatically identify based on calling context.

## Skills & Tool Dependencies

### Associated Skills
*Currently, this agent focuses on planning and design. Future skills may include:*
- Execution-focused skills that implement the plans created by this agent

### Tools Available
- **Read/Write/Edit**: Read specifications, write planning documents
- **Grep/Glob**: Search codebase for patterns and examples
- **WebSearch/WebFetch**: Research best practices and documentation

### Responsibility Boundaries
**This Agent ({agent_id})**:
- Planning, architecture design, and strategy formulation
- Creating structured specifications and blueprints

**Other Agents/Skills Handle**:
- F0-F9: Collaborative planning across development lifecycle
- Execution skills: Actual implementation and coding
"""

    # Find collaboration section to insert before it
    collab_pattern = r"(\n## Collaboration Protocol|\n## Collaboration Guidelines|\n## Quality Standards)"
    if re.search(collab_pattern, content):
        content = re.sub(collab_pattern, f"{element7}\\1", content, count=1)
    else:
        # Fallback: append before last section
        content = content.rstrip() + f"\n{element7}\n"

    # Construct Element 13 (Precautions & Notes) and Output Path - append at end
    element13 = f"""
## Output Path Convention

All planning outputs follow standardized paths:
```
output/[项目名]/{agent_id}/
├── plans/          # Planning configs (JSON/YAML)
├── results/        # Final documents (MD format)
├── logs/           # Planning process logs
└── metadata/       # Traceability metadata
```

**Example Project Names**:
{chr(10).join(f"- \"{example}\"" for example in domain['project_examples'])}

## Precautions & Notes

<precautions>
### Pre-configured Warnings
1. ⚠️ **Quality standards are non-negotiable** - All outputs must meet defined quality criteria before delivery
2. ⚠️ **Planning precedes execution** - Never skip the planning phase; rushed plans lead to implementation failures
3. ⚠️ **Documentation is mandatory** - All decisions and rationale must be documented for future reference
4. ⚠️ **Collaboration is essential** - Proactively coordinate with other agents; siloed work creates integration issues
5. ⚠️ **Continuous improvement** - Learn from each project; update processes and standards based on outcomes

### Runtime Learnings (动态更新)
- Document lessons learned from each project execution
- Identify patterns that work well and anti-patterns to avoid
- Continuously refine planning templates and processes

### Update Protocol
When encountering situations worth recording:
- Propose update: "建议添加注意事项: [description]"
- User reviews and approves update
- Update this section accordingly
</precautions>
"""

    # Append at the end
    content = content.rstrip() + f"\n{element13}\n"

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ {agent_id} supplemented successfully")

if __name__ == "__main__":
    agents = ["F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]
    for agent in agents:
        try:
            add_elements_to_agent(agent)
        except Exception as e:
            print(f"❌ Error processing {agent}: {e}")

    print("\n🎉 All agents supplemented!")
