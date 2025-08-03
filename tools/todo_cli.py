#\!/usr/bin/env python3
"""
Command-line interface for TodoWrite tool
Usage: python todo_cli.py [command] [options]
"""

import argparse
import json
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from todo_writer import TodoWriter, quick_complete_task


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="TodoWrite CLI - Task management with git integration")
    
    # Global options
    parser.add_argument('--tasks-file', '-f', help='Path to tasks file (default: .ralex_tasks.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create task command
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument('id', help='Task ID')
    create_parser.add_argument('name', help='Task name')
    create_parser.add_argument('description', help='Task description')
    create_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], 
                              default='medium', help='Task priority')
    
    # Update task command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('id', help='Task ID')
    update_parser.add_argument('--name', help='New task name')
    update_parser.add_argument('--description', help='New task description')
    update_parser.add_argument('--status', choices=['pending', 'in_progress', 'completed', 'blocked'],
                              help='New task status')
    update_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'],
                              help='New task priority')
    
    # Complete task command
    complete_parser = subparsers.add_parser('complete', help='Mark task as completed and create git commit')
    complete_parser.add_argument('id', help='Task ID')
    complete_parser.add_argument('--verification', '-v', action='append', 
                                help='Verification step (can be used multiple times)')
    complete_parser.add_argument('--files', '-m', action='append',
                                help='Modified file (can be used multiple times)')
    complete_parser.add_argument('--next', help='Next task information')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=['pending', 'in_progress', 'completed', 'blocked'],
                            help='Filter by status')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Get task command
    get_parser = subparsers.add_parser('get', help='Get a specific task')
    get_parser.add_argument('id', help='Task ID')
    get_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', help='Task ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize TodoWriter
    writer = TodoWriter(args.tasks_file)
    
    try:
        if args.command == 'create':
            result = writer.create_task(args.id, args.name, args.description, args.priority)
            print_result(result)
            
        elif args.command == 'update':
            updates = {}
            if args.name:
                updates['name'] = args.name
            if args.description:
                updates['description'] = args.description
            if args.status:
                updates['status'] = args.status
            if args.priority:
                updates['priority'] = args.priority
                
            if not updates:
                print("Error: No updates specified")
                return
                
            result = writer.update_task(args.id, **updates)
            print_result(result)
            
        elif args.command == 'complete':
            result = writer.complete_task(
                args.id,
                verification_steps=args.verification or [],
                files_modified=args.files or [],
                next_task_info=args.next or ""
            )
            print_result(result)
            
        elif args.command == 'list':
            result = writer.list_tasks(args.status)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print_task_list(result)
                
        elif args.command == 'get':
            result = writer.get_task(args.id)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print_task_details(result)
                
        elif args.command == 'delete':
            result = writer.delete_task(args.id)
            print_result(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def print_result(result):
    """Print command result"""
    if result.get('error'):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    elif result.get('warning'):
        print(f"Warning: {result['warning']}")
    
    if result.get('success'):
        print("Success\!")
        
    if 'git_commit' in result:
        git_result = result['git_commit']
        if git_result.get('success'):
            print(f"Git commit created: {git_result.get('commit_hash', 'unknown')}")
            push_result = git_result.get('push_result', {})
            print(f"Push status: {push_result.get('status', 'unknown')}")
            if push_result.get('message'):
                print(f"Push message: {push_result['message']}")
        elif git_result.get('error'):
            print(f"Git commit failed: {git_result['error']}")


def print_task_list(result):
    """Print formatted task list"""
    if result.get('error'):
        print(f"Error: {result['error']}", file=sys.stderr)
        return
        
    tasks = result.get('tasks', {})
    count = result.get('count', 0)
    
    print(f"Found {count} task(s):")
    print()
    
    for task_id, task in tasks.items():
        status_icon = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'blocked': '❌'
        }.get(task['status'], '❓')
        
        priority_icon = {
            'low': '🔹',
            'medium': '🔸',
            'high': '🔶',
            'critical': '🔴'
        }.get(task['priority'], '⚪')
        
        print(f"{status_icon} {priority_icon} [{task['id']}] {task['name']}")
        print(f"   Status: {task['status']} | Priority: {task['priority']}")
        print(f"   Created: {task['created_at']}")
        if task['description']:
            print(f"   Description: {task['description']}")
        print()


def print_task_details(result):
    """Print detailed task information"""
    if result.get('error'):
        print(f"Error: {result['error']}", file=sys.stderr)
        return
        
    task = result.get('task', {})
    
    status_icon = {
        'pending': '⏳',
        'in_progress': '🔄',
        'completed': '✅',
        'blocked': '❌'
    }.get(task['status'], '❓')
    
    priority_icon = {
        'low': '🔹',
        'medium': '🔸',
        'high': '🔶',
        'critical': '🔴'
    }.get(task['priority'], '⚪')
    
    print(f"{status_icon} {priority_icon} Task {task['id']}: {task['name']}")
    print(f"Status: {task['status']}")
    print(f"Priority: {task['priority']}")
    print(f"Created: {task['created_at']}")
    print(f"Updated: {task['updated_at']}")
    print()
    print("Description:")
    print(f"  {task['description']}")
    
    if task.get('verification_steps'):
        print()
        print("Verification Steps:")
        for step in task['verification_steps']:
            print(f"  • {step}")
    
    if task.get('files_modified'):
        print()
        print("Files Modified:")
        for file in task['files_modified']:
            print(f"  • {file}")
    
    if task.get('next_task_info'):
        print()
        print("Next Task Info:")
        print(f"  {task['next_task_info']}")


if __name__ == '__main__':
    main()
EOF < /dev/null