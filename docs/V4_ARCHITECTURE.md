# Ralex V4 Architecture Documentation

**🏗️ Complete technical architecture for voice-driven AI orchestration platform**

## 🎯 **System Overview**

Ralex V4 transforms from a simple AI assistant into a comprehensive orchestration platform that seamlessly coordinates multiple AI tools through natural voice commands while maintaining persistent context and intelligent automation.

## 🏛️ **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                     Ralex V4 System Architecture               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🎙️ Voice Input (Web Speech API)                                │
│                            ↓                                    │
│  📱 Open WebUI Interface (Mobile + Desktop)                     │
│                            ↓                                    │
│  🧠 Ralex V4 Orchestrator ←→ 📝 Context Management System       │
│                            ↓           ↓                        │
│  📋 AgentOS Enhancement ←──┴─── 🔍 Context7 Integration         │
│                            ↓                                    │
│  🎯 LiteLLM Model Router                                        │
│                            ↓                                    │
│  🔧 OpenCode Execution Engine                                   │
│                            ↓                                    │
│  📊 Results Processing + Context Update                         │
│                            ↓                                    │
│  🔄 GitHub Context Sync + WebSocket UI Updates                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 **Core Components**

### **1. Voice Interface Layer**

#### **Technology Stack:**
- **Frontend**: Open WebUI (Svelte + TailwindCSS)
- **Voice Recognition**: Web Speech API with fallback support
- **Communication**: WebSocket for real-time updates
- **Mobile Support**: Progressive Web App (PWA) capabilities

#### **Component Structure:**
```
ralex-webui/
├── src/lib/components/voice/
│   ├── VoiceInput.svelte          # Voice recognition component
│   ├── VoiceCommands.svelte       # Command suggestion UI
│   └── VoiceStatus.svelte         # Recognition status display
├── src/lib/stores/
│   ├── voiceStore.js              # Voice state management
│   └── sessionStore.js            # Session context state
└── src/routes/
    ├── (app)/+page.svelte         # Main voice interface
    └── mobile/+page.svelte        # Mobile-optimized interface
```

#### **Key Features:**
- **Cross-browser compatibility** with graceful degradation
- **Mobile-optimized touch interface** with gesture support
- **Real-time transcription feedback** during voice input
- **Auto-submit patterns** based on command endings
- **Offline capability** with cached functionality

### **2. Orchestrator Core**

#### **Architecture Pattern:**
The orchestrator follows a **Command Pattern** with **Pipeline Architecture** for processing voice commands through multiple enhancement stages.

```python
# ralex_core/v4_orchestrator.py
class RalexV4Orchestrator:
    """Central orchestration engine for all V4 operations"""
    
    def __init__(self):
        self.context_manager = ContextManager()
        self.command_parser = CommandParser()
        self.agentos_enhancer = AgentOSEnhancer()
        self.litellm_router = LiteLLMRouter()
        self.opencode_client = OpenCodeClient()
        self.security_manager = SecurityManager()
        self.workflow_engine = WorkflowEngine()
    
    async def process_voice_command(self, 
                                  command: str, 
                                  session_id: str,
                                  user_context: dict = None) -> ProcessingResult:
        """Main orchestration pipeline"""
        
        # 1. Parse and validate command
        parsed_command = await self.command_parser.parse(command)
        security_check = await self.security_manager.validate(parsed_command)
        
        if not security_check.is_safe:
            return ProcessingResult.error(security_check.reason)
        
        # 2. Load relevant context
        context = await self.context_manager.load_context(
            session_id, parsed_command
        )
        
        # 3. Enhance with AgentOS standards
        enhanced_prompt = await self.agentos_enhancer.enhance(
            parsed_command, context
        )
        
        # 4. Route to appropriate model
        model_selection = await self.litellm_router.select_model(
            enhanced_prompt, context.complexity
        )
        
        # 5. Execute via OpenCode
        execution_result = await self.opencode_client.execute(
            enhanced_prompt, model_selection, context
        )
        
        # 6. Update context with results
        await self.context_manager.update_context(
            session_id, execution_result, parsed_command
        )
        
        return ProcessingResult.success(execution_result)
```

#### **Pipeline Stages:**
1. **Command Parsing**: Natural language → Structured intent
2. **Security Validation**: Safety checks and permission verification
3. **Context Loading**: Relevant project and session context
4. **AgentOS Enhancement**: Standards application and prompt optimization
5. **Model Routing**: Intelligent model selection based on complexity
6. **OpenCode Execution**: File operations and shell commands
7. **Context Update**: Learning and context persistence
8. **Response Generation**: User feedback and UI updates

### **3. Context Management System**

#### **Storage Architecture:**
The context system uses a **hybrid approach** combining structured storage with human-readable markdown files.

```
.ralex/
├── context/
│   ├── project_understanding.md    # Overall project context
│   ├── conversation_history.md     # Key decisions and patterns
│   ├── user_patterns.md           # Coding style and preferences
│   ├── file_relationships.md      # Code dependencies mapping
│   └── security_audit.md          # Security decisions log
├── sessions/
│   ├── 2025-01-15-auth-system.md  # Individual session contexts
│   ├── 2025-01-16-payment-api.md  # Feature-specific contexts
│   └── ...
├── cache/
│   ├── documentation_cache.json   # Context7 doc cache
│   ├── model_performance.json     # LiteLLM routing optimization
│   └── pattern_analysis.json      # User behavior analysis
└── config/
    ├── preferences.yaml           # User configuration
    ├── workflows.yaml             # Custom workflow definitions
    └── security_rules.yaml        # Project-specific security rules
```

#### **Context Management Implementation:**
```python
# ralex_core/context_manager.py
class ContextManager:
    """Intelligent context loading and management"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.context_dir = project_path / ".ralex"
        self.git_sync = GitSyncManager(self.context_dir)
        self.compressor = ContextCompressor()
        
    async def load_context(self, 
                          session_id: str, 
                          command: ParsedCommand) -> ContextPackage:
        """Load relevant context based on command analysis"""
        
        # Analyze command for context requirements
        context_requirements = self._analyze_context_needs(command)
        
        # Load base project context
        project_context = await self._load_project_context()
        
        # Load session-specific context
        session_context = await self._load_session_context(session_id)
        
        # Load file-specific context if files referenced
        file_context = await self._load_file_context(
            context_requirements.referenced_files
        )
        
        # Load relevant documentation via Context7
        documentation = await self._load_documentation(
            context_requirements.imports,
            context_requirements.technologies
        )
        
        return ContextPackage(
            project=project_context,
            session=session_context,
            files=file_context,
            documentation=documentation,
            user_patterns=await self._load_user_patterns()
        )
```

#### **Context Intelligence Features:**
- **Relevance Scoring**: Load only context relevant to current command
- **Compression Strategy**: Automatic summarization of old context
- **Cross-Session Learning**: Pattern recognition across sessions
- **Predictive Loading**: Preload likely-needed context
- **Conflict Resolution**: Smart merging of context changes

### **4. AgentOS Integration**

#### **Enhanced Prompt Pipeline:**
The AgentOS integration provides intelligent prompt enhancement based on project context and user patterns.

```python
# ralex_core/agentos_v4_integration.py
class AgentOSV4Enhancer:
    """Context-aware prompt enhancement with AgentOS standards"""
    
    def __init__(self, agent_os_path: Path):
        self.standards_loader = StandardsLoader(agent_os_path)
        self.pattern_analyzer = PatternAnalyzer()
        self.context7_client = Context7Client()
        
    async def enhance(self, 
                     command: ParsedCommand, 
                     context: ContextPackage) -> EnhancedPrompt:
        """Multi-stage prompt enhancement"""
        
        # 1. Analyze command complexity and requirements
        complexity_analysis = await self._analyze_complexity(command, context)
        
        # 2. Select relevant standards
        relevant_standards = await self._select_standards(
            context.project.languages,
            context.project.frameworks,
            complexity_analysis.requirements
        )
        
        # 3. Load dynamic documentation
        documentation = await self.context7_client.get_relevant_docs(
            context.imports,
            command.intent
        )
        
        # 4. Apply user patterns and preferences
        user_adaptations = await self._apply_user_patterns(
            command, context.user_patterns
        )
        
        # 5. Build enhanced prompt
        enhanced_prompt = PromptBuilder()
            .add_standards(relevant_standards)
            .add_context(context.most_relevant())
            .add_documentation(documentation)
            .add_user_patterns(user_adaptations)
            .add_original_request(command.original_text)
            .build()
        
        return EnhancedPrompt(
            content=enhanced_prompt,
            complexity=complexity_analysis,
            estimated_tokens=len(enhanced_prompt.split()),
            context_sources=context.get_sources()
        )
```

#### **Standards Selection Logic:**
- **File-Type Based**: Python files → Python standards, JS → JS standards
- **Complexity Based**: Complex tasks → Testing + Error handling standards
- **Project Based**: Detected frameworks → Framework-specific standards
- **User Based**: Learned preferences → Preferred patterns and styles

### **5. LiteLLM Model Router**

#### **Intelligent Routing Algorithm:**
```python
# ralex_core/litellm_v4_router.py
class LiteLLMV4Router:
    """Enhanced model routing with context awareness"""
    
    def __init__(self):
        self.model_registry = ModelRegistry()
        self.cost_tracker = CostTracker()
        self.performance_analyzer = PerformanceAnalyzer()
        
    async def select_model(self, 
                          enhanced_prompt: EnhancedPrompt,
                          budget_context: BudgetContext) -> ModelSelection:
        """Multi-factor model selection"""
        
        # Analyze prompt requirements
        requirements = PromptAnalyzer.analyze(enhanced_prompt)
        
        # Get available models within budget
        available_models = await self._get_available_models(
            budget_context.remaining_budget,
            requirements.estimated_cost
        )
        
        # Score models based on multiple factors
        model_scores = {}
        for model in available_models:
            score = await self._calculate_model_score(
                model, requirements, enhanced_prompt
            )
            model_scores[model] = score
        
        # Select best model
        selected_model = max(model_scores, key=model_scores.get)
        
        return ModelSelection(
            model=selected_model,
            estimated_cost=requirements.estimated_cost,
            reasoning=self._build_selection_reasoning(
                selected_model, model_scores, requirements
            )
        )
    
    async def _calculate_model_score(self, 
                                   model: Model, 
                                   requirements: PromptRequirements,
                                   enhanced_prompt: EnhancedPrompt) -> float:
        """Multi-factor scoring algorithm"""
        
        # Base capability score
        capability_score = model.capability_ratings.get(
            requirements.task_type, 0.5
        )
        
        # Cost efficiency score (inverse of cost per token)
        cost_score = 1.0 / (model.cost_per_token * requirements.estimated_tokens)
        
        # Historical performance score
        performance_score = await self.performance_analyzer.get_score(
            model, requirements.task_type, enhanced_prompt.complexity
        )
        
        # Context compatibility score
        context_score = self._calculate_context_compatibility(
            model, enhanced_prompt.context_sources
        )
        
        # Weighted combination
        total_score = (
            capability_score * 0.4 +
            cost_score * 0.2 +
            performance_score * 0.3 +
            context_score * 0.1
        )
        
        return total_score
```

#### **Model Performance Learning:**
- **Success Rate Tracking**: Monitor completion rates by task type
- **Quality Assessment**: Track user satisfaction and code quality
- **Cost Efficiency**: Analyze cost vs. value for different models
- **Context Optimization**: Learn which models work best with specific contexts

### **6. OpenCode Integration**

#### **Safe Execution Architecture:**
```python
# ralex_core/opencode_client.py
class OpenCodeClient:
    """Safe OpenCode CLI integration with comprehensive error handling"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.security_manager = SecurityManager()
        self.backup_manager = BackupManager()
        self.session_manager = OpenCodeSessionManager()
        
    async def execute(self, 
                     enhanced_prompt: EnhancedPrompt,
                     model_selection: ModelSelection,
                     context: ContextPackage) -> ExecutionResult:
        """Safe execution with comprehensive error handling"""
        
        # 1. Pre-execution validation
        validation_result = await self.security_manager.validate_execution(
            enhanced_prompt, context
        )
        
        if not validation_result.is_safe:
            return ExecutionResult.blocked(validation_result.reason)
        
        # 2. Create backup point
        backup_id = await self.backup_manager.create_snapshot()
        
        try:
            # 3. Execute via OpenCode CLI
            execution_result = await self._execute_opencode_command(
                enhanced_prompt, model_selection
            )
            
            # 4. Validate results
            validation = await self._validate_execution_results(
                execution_result
            )
            
            if validation.has_errors:
                # Rollback on validation failure
                await self.backup_manager.restore_snapshot(backup_id)
                return ExecutionResult.error(validation.errors)
            
            # 5. Success - clean up backup
            await self.backup_manager.cleanup_snapshot(backup_id)
            
            return ExecutionResult.success(execution_result)
            
        except Exception as e:
            # Rollback on any exception
            await self.backup_manager.restore_snapshot(backup_id)
            return ExecutionResult.exception(e)
```

#### **OpenCode CLI Integration:**
- **Non-Interactive Mode**: Programmatic execution without user prompts
- **Structured Output**: JSON responses for programmatic processing
- **Session Management**: Persistent OpenCode sessions for context
- **Error Handling**: Comprehensive error detection and recovery

### **7. Context7 Integration**

#### **MCP Client Architecture:**
```python
# ralex_core/context7_client.py
class Context7Client:
    """Model Context Protocol client for dynamic documentation"""
    
    def __init__(self):
        self.mcp_client = MCPClient("context7-server")
        self.doc_cache = DocumentationCache()
        self.version_tracker = VersionTracker()
        
    async def get_relevant_docs(self, 
                              imports: List[str],
                              intent: CommandIntent) -> DocumentationSet:
        """Fetch relevant documentation based on context"""
        
        # Analyze imports for library requirements
        libraries = await self._analyze_imports(imports)
        
        # Get version information
        versions = await self.version_tracker.get_versions(libraries)
        
        # Fetch documentation for each library
        documentation = {}
        for library, version in versions.items():
            # Check cache first
            cached_docs = await self.doc_cache.get(library, version)
            if cached_docs:
                documentation[library] = cached_docs
                continue
            
            # Fetch from Context7 MCP server
            docs = await self.mcp_client.request_documentation(
                library=library,
                version=version,
                intent=intent.type,
                keywords=intent.keywords
            )
            
            # Cache for future use
            await self.doc_cache.store(library, version, docs)
            documentation[library] = docs
        
        return DocumentationSet(documentation)
```

#### **Documentation Intelligence:**
- **Version-Aware**: Fetch docs specific to installed library versions
- **Intent-Based**: Filter documentation based on command intent
- **Performance Optimized**: Aggressive caching with smart invalidation
- **Relevance Scoring**: Prioritize most relevant documentation sections

## 🔄 **Data Flow Architecture**

### **Command Processing Flow:**
```
🎙️ Voice Input: "Fix the authentication bug in user_auth.py, execute"
                                    ↓
📝 Command Parsing: {
    intent: "fix_bug",
    files: ["user_auth.py"],
    auto_submit: true,
    complexity: "moderate"
}
                                    ↓
🔍 Context Loading: {
    project_context: "Django web app with JWT auth",
    session_context: "Working on user management features",
    file_context: "user_auth.py content and related files",
    documentation: "Django auth docs, JWT library docs"
}
                                    ↓
📋 AgentOS Enhancement: {
    standards: ["python", "django", "testing", "security"],
    enhanced_prompt: "Fix authentication bug following Django best practices...",
    complexity_analysis: "Moderate - requires security awareness"
}
                                    ↓
🎯 Model Selection: {
    selected_model: "anthropic/claude-3-sonnet",
    reasoning: "Security-sensitive bug fix requires high-capability model",
    estimated_cost: "$0.015"
}
                                    ↓
🔧 OpenCode Execution: {
    command: "analyze user_auth.py for authentication bugs and fix",
    backup_created: true,
    execution_safe: true
}
                                    ↓
📊 Result Processing: {
    files_modified: ["user_auth.py", "tests/test_auth.py"],
    git_commit: "fix: resolve JWT token validation bug",
    tests_passed: true,
    context_updated: true
}
                                    ↓
🔄 UI Update: WebSocket notification to user with results
```

### **Context Update Flow:**
```
📝 New Learning: User prefers pytest over unittest
                                    ↓
🧠 Pattern Analysis: Detect testing framework preference
                                    ↓
💾 Context Storage: Update user_patterns.md with preference
                                    ↓
🔄 Git Sync: Commit context changes to GitHub
                                    ↓
📱 Cross-Device Sync: Context available on all user devices
```

## 🛡️ **Security Architecture**

### **Multi-Layer Security Model:**

#### **Layer 1: Command Validation**
```python
class SecurityManager:
    """Comprehensive security validation"""
    
    SAFE_OPERATIONS = {
        "read_file", "write_file", "create_file", "list_directory",
        "git_status", "git_add", "git_commit", "git_push",
        "run_tests", "check_lint", "format_code", "install_package"
    }
    
    DANGEROUS_OPERATIONS = {
        "rm -rf", "sudo", "chmod 777", "dd if=", "format",
        "fdisk", "mkfs", "shutdown", "reboot", "kill -9"
    }
    
    CONFIRMATION_REQUIRED = {
        "delete_file", "git_reset --hard", "deploy",
        "database_migration", "system_update"
    }
```

#### **Layer 2: File System Boundaries**
- **Project Root Enforcement**: All operations confined to project directory
- **Path Traversal Prevention**: Block "../" and absolute paths outside project
- **Hidden File Protection**: Restrict access to sensitive hidden files
- **Git Repository Validation**: Ensure operations only in valid git repos

#### **Layer 3: Backup and Recovery**
- **Automatic Snapshots**: Git snapshots before any file modifications
- **Rollback Capability**: One-click recovery from failed operations
- **Context Backup**: Regular backup of context files to GitHub
- **Audit Trail**: Complete log of all operations for security review

#### **Layer 4: Runtime Monitoring**
- **Operation Monitoring**: Real-time monitoring of all system calls
- **Anomaly Detection**: Unusual patterns trigger security alerts  
- **Rate Limiting**: Prevent abuse through request rate limiting
- **Session Security**: Secure session management and timeout handling

## 📊 **Performance Architecture**

### **Performance Optimization Strategies:**

#### **Caching Layer:**
```python
class PerformanceCache:
    """Multi-level caching for optimal performance"""
    
    def __init__(self):
        self.context_cache = LRUCache(maxsize=100)
        self.documentation_cache = TTLCache(maxsize=500, ttl=3600)
        self.model_response_cache = TTLCache(maxsize=200, ttl=1800)
        self.file_content_cache = TTLCache(maxsize=50, ttl=300)
```

#### **Async Processing:**
- **Parallel Context Loading**: Load project, session, and file context concurrently
- **Background Sync**: GitHub context sync happens asynchronously
- **Preemptive Caching**: Predictive loading of likely-needed resources
- **WebSocket Streaming**: Real-time UI updates during long operations

#### **Resource Management:**
- **Memory Optimization**: Efficient context compression and cleanup
- **Network Optimization**: Batch API calls and minimize requests
- **Disk Optimization**: Efficient file operations with minimal I/O
- **CPU Optimization**: Lazy loading and on-demand processing

## 🔧 **Deployment Architecture**

### **Containerized Deployment:**
```yaml
# docker-compose.v4.yml
version: '3.8'
services:
  ralex-orchestrator:
    build: .
    ports: ["8000:8000"]
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - RALEX_ENV=production
    volumes:
      - ./data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    
  ralex-webui:
    build: ./ralex-webui
    ports: ["3000:3000"]
    environment:
      - OPENAI_API_BASE_URL=http://ralex-orchestrator:8000/v4
    depends_on: [ralex-orchestrator]
    
  context7-mcp:
    image: upstash/context7:latest
    ports: ["8001:8001"]
    environment:
      - CONTEXT7_CONFIG_PATH=/config/context7.yaml
    volumes:
      - ./config:/config
    
  nginx:
    image: nginx:alpine
    ports: ["443:443", "80:80"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /var/lib/tailscale/certs:/etc/nginx/certs:ro
    depends_on: [ralex-webui, ralex-orchestrator]
```

### **High Availability Features:**
- **Health Checks**: Comprehensive health monitoring for all services
- **Auto-Restart**: Automatic restart of failed components
- **Graceful Degradation**: System continues operating with reduced functionality
- **Backup Services**: Fallback mechanisms for critical components

## 📈 **Monitoring & Observability**

### **Metrics Collection:**
```python
class MetricsCollector:
    """Comprehensive performance and usage metrics"""
    
    def __init__(self):
        self.latency_tracker = LatencyTracker()
        self.cost_tracker = CostTracker()
        self.usage_tracker = UsageTracker()
        self.error_tracker = ErrorTracker()
    
    async def track_command_execution(self, 
                                    command: str,
                                    execution_time: float,
                                    success: bool,
                                    cost: float):
        """Track command execution metrics"""
        
        await self.latency_tracker.record(
            command_type=self._classify_command(command),
            duration=execution_time
        )
        
        await self.cost_tracker.record(
            command=command,
            cost=cost,
            timestamp=datetime.now()
        )
        
        await self.usage_tracker.record(
            feature_used=self._extract_features(command),
            success=success
        )
        
        if not success:
            await self.error_tracker.record(
                command=command,
                error_type=self._classify_error(command)
            )
```

### **Real-Time Dashboard:**
- **Performance Metrics**: Latency, throughput, success rates
- **Cost Analytics**: Real-time spending, budget alerts, cost optimization
- **Usage Patterns**: Feature usage, user behavior analysis
- **System Health**: Component status, error rates, resource usage

## 🔄 **Future Architecture Considerations**

### **Scalability Path:**
- **Microservices**: Split orchestrator into specialized services
- **Load Balancing**: Multiple orchestrator instances for high load
- **Database Integration**: Structured storage for large-scale context
- **Cloud Deployment**: AWS/GCP deployment for global availability

### **Advanced Features:**
- **Multi-User Support**: Team collaboration and shared contexts
- **Plugin Architecture**: Third-party tool integration framework
- **Advanced AI**: Custom fine-tuned models for specific use cases
- **Enterprise Features**: SSO, RBAC, compliance reporting

---

## ✅ **Architecture Complete**

This architecture provides a robust, scalable, and secure foundation for Ralex V4 as a world-class voice-driven AI orchestration platform. The modular design enables incremental development while maintaining system integrity and performance.

---

*Generated: January 2025*  
*Version: 4.0.0-architecture*  
*Status: Implementation ready*