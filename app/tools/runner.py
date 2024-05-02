import json
from app.messages import system_message, user_message
from app.tools.run_command import run_command
from app.tools.get_file_contents import get_file_contents
from app.tools.create_file import create_file
from app.tools.run_python import run_python
from app.tools.human_in_middle import human_in_middle
from app.prompts.create_project import (
    prereq_action_plan_prompt,
    create_the_action_plan_prompt,
    summarize_action_plan_prompt,
    troubelshoot_tool_prompt,
)
from app.gpt import gpt_messages
import logging

log = logging.getLogger("app")


def run_tool(tool, source_path, troubleshooting=False):
    log.info(f"Running Command: {tool['tool']}::{tool['params']}")
    if tool["tool"] == "run_command":
        result = run_command(tool["params"], source_path)
    elif tool["tool"] == "get_file_contents":
        result = get_file_contents(source_path, tool["params"])
    elif tool["tool"] == "create_file":
        result = create_file(f"{source_path}", tool["params"][0], tool["params"][1])
    elif tool["tool"] == "run_python":
        result = run_python(tool["params"])
    elif tool["tool"] == "human_in_middle":
        result = human_in_middle(tool["params"])

    log.info(f"Result: {result}")
    if "error" in json.dumps(result).lower():
        troubleshoot_tool(tool, result, source_path, troubleshooting)

    return f"Output from tool '{tool['tool']}' with params '{tool['params']}':\n{result}\n\n"


previous_attempts = []


def troubleshoot_tool(tool, output, source_path, retry=False):
    global previous_attempts
    previous = ""
    if not retry:
        previous_attempts = []
        previous = ""

    previous = "\n\n".join(previous_attempts)
    if previous:
        previous = f"PREVIOUS ATTEMPTS:\n{previous}\n\n"

    messages = [
        system_message(troubelshoot_tool_prompt()),
        user_message(
            f"{previous}TOOL: {tool['tool']}::{tool['params']}\nOUTPUT: {output}\n\n"
        ),
    ]
    log.info("Running prompt troubelshoot_tool_prompt")
    response = gpt_messages(messages=messages, in_json=True)
    actions = json.loads(response)["actions"]
    log.info(f"Troubleshooting with {len(actions)} actions")
    for task in actions:
        previous_attempts.append(
            f"TOOL: {tool['tool']}::{tool['params']}\nOUTPUT: {output}\n\n"
        )
        run_tool(task, source_path, True)


def run_tools(tools, source_path, troubleshooting=False):
    step_output = ""
    for tool in tools:
        step_output += run_tool(tool, source_path, troubleshooting)
    return step_output


# def perform_action(task, task_output, step_output, output_path):
#     log.info(task["action"])
#     user_prefix = ""
#     if task_output:
#         user_prefix = f"Previous Tasks:\n{task_output}\n\n"
#     messages = [
#         system_message(create_the_action_plan_prompt()),
#         user_message(
#             f"{user_prefix}YOUR NEXT TASK\nName: {task['action']}\nDetails: {task['details']}"
#         ),
#     ]
#     response = gpt_messages(messages=messages, in_json=True)
#     log.info("\n*****\n  Perform the Action:")
#     log.info(response)
#     log.info("\n\n")
#     response = json.loads(response)
#     for tool in response["tools"]:
#         step_output += run_tool(tool, output_path)
#     return step_output


def get_existing_summaries(all_action_plans):
    summaries = "\n\n".join(
        [
            f'Summary of Action Plan: {ap["action_plan"]}\n{ap["summary"]}'
            for ap in all_action_plans
            if "summary" in ap
        ]
    )
    return summaries


def get_prerequisites(action_plan, prefix, all_action_plans, target_path):
    log.info(action_plan["action_plan"])
    summaries = get_existing_summaries(all_action_plans)
    if summaries:
        summaries = f"ACTION PLAN SUMMARIES:\n{summaries}"
    messages = [
        system_message(prereq_action_plan_prompt()),
        user_message(
            f"{prefix}{summaries}ACTION PLAN\nName: {action_plan['action_plan']}\nDetails: {action_plan['details']}"
        ),
    ]
    log.info("Running prompt prereq_action_plan_prompt")
    response = gpt_messages(messages=messages, in_json=True)
    log.info("\n*****\nPrerequisites Action Plan:")
    log.info(response)

    tools = json.loads(response)
    if "actions" in tools and len(tools["actions"]) > 0:
        for tool in tools["actions"]:
            tool["output"] = run_tool(tool, target_path)

    return tools


def create_detailed_action_plan(action_plan, prefix, prereqs, all_action_plans):
    return """{\n  "actions": [\n    {\n      "tool": "create_file",\n      "params": [\n        "README.md",\n        "# Dan\'s Diet\\n\\nThis project aims to simplify the process of sharing dietary preferences and restrictions. Built with ReactJS, AWS Lambda, RDS (PostgreSQL), AWS Amplify, and Cognito.\\n\\n## Getting Started\\n\\nFollow the instructions below to set up the project locally.\\n\\n### Prerequisites\\n\\n- Node.js\\n- AWS CLI\\n- Amplify CLI\\n\\n### Installation\\n\\n1. Clone the repository.\\n2. Install dependencies: `npm install`.\\n3. Set up AWS resources.\\n4. Start the development server: `npm start`."\n      ],\n      "order": 1\n    },\n    {\n      "tool": "human_in_middle",\n      "params": [\n        "1. Run `amplify init` to initialize the AWS Amplify project.\\n2. Follow the prompts to configure the project. Use the project name \'DansDiet\'. Choose the default editor, and make sure to select \'AWS profile\' for the authentication method.\\n3. Return the Amplify project initialization output."\n      ],\n      "order": 2\n    },\n    {\n      "tool": "human_in_middle",\n      "params": [\n        "1. Set up AWS Cognito for authentication.\\n2. Run `amplify add auth` and follow the prompts to create a user pool with standard attributes. Ensure to configure both email and password as sign-in methods.\\n3. Return the confirmation that Cognito has been set up with the user pool ID."\n      ],\n      "order": 3\n    },\n    {\n      "tool": "human_in_middle",\n      "params": [\n        "1. Set up AWS RDS with PostgreSQL.\\n2. Navigate to the AWS Management Console, select RDS, and create a new PostgreSQL database. Choose the free tier options for cost-efficiency.\\n3. Configure the database with a secure password and remember to allow access from AWS Lambda functions by setting the correct VPC security groups.\\n4. Return the database endpoint and credentials (host, database name, username, password)."\n      ],\n      "order": 4\n    },\n    {\n      "tool": "human_in_middle",\n      "params": [\n        "1. Initialize the AWS Lambda function for backend logic.\\n2. Run `amplify add function` and follow the prompts to create a new Lambda function. Choose \'Serverless function\' as the function template and provide a meaningful name.\\n3. Ensure to configure the function with access to AWS RDS by selecting the appropriate permissions.\\n4. Return the confirmation that the Lambda function has been created."\n      ],\n      "order": 5\n    },\n    {\n      "tool": "create_file",\n      "params": [\n        "amplify/backend/api/dansdiet/schema.graphql",\n        "# GraphQL schema definition for Dan\'s Diet\\n\\ntype Diet {\\n  id: ID!\\n  name: String!\\n  restrictions: [String]\\n  allowedFoods: [String]\\n  substitutions: [String]\\n}\\n\\ntype Query {\\n  getDiet(id: ID!): Diet\\n}\\n\\ntype Mutation {\\n  createDiet(name: String!, restrictions: [String], allowedFoods: [String], substitutions: [String]): Diet\\n}"\n      ],\n      "order": 6\n    },\n    {\n      "tool": "human_in_middle",\n      "params": [\n        "1. Configure CI/CD pipelines using AWS Amplify.\\n2. Navigate to the AWS Amplify Console, connect your GitHub repository, and set up a new Amplify app.\\n3. Follow the prompts to configure the build settings, making sure to include build commands for both the frontend and backend resources.\\n4. Return the URL of the deployed application once the initial build and deployment are complete."\n      ],\n      "order": 7\n    },\n    {\n      "tool": "create_file",\n      "params": [\n        "src/index.js",\n        "import React from \'react\';\\nimport ReactDOM from \'react-dom\';\\nimport \'./index.css\';\\nimport App from \'./App\';\\n\\nReactDOM.render(\\n  <React.StrictMode>\\n    <App />\\n  </React.StrictMode>,\\n  document.getElementById(\'root\')\\n);"\n      ],\n      "order": 8\n    },\n    {\n      "tool": "create_file",\n      "params": [\n        "src/App.js",\n        "import React from \'react\';\\nimport { BrowserRouter as Router, Route, Switch } from \'react-router-dom\';\\n\\nfunction App() {\\n  return (\\n    <Router>\\n      <div className=\'App\'>\\n        <Switch>\\n          {/* Define routes here */}\\n        </Switch>\\n      </div>\\n    </Router>\\n  );\\n}\\n\\nexport default App;"\n      ],\n      "order": 9\n    },\n    {\n      "tool": "run_command",\n      "params": [\n        "npm install react-router-dom @material-ui/core"\n      ],\n      "order": 10\n    }\n  ]\n}"""
    log.info(action_plan["action_plan"])
    summaries = get_existing_summaries(all_action_plans)
    if summaries:
        summaries = f"ACTION PLAN SUMMARIES:\n{summaries}"

    user_msg = f"{prefix}{summaries}PREREQUISITES:\n{prereqs}\n\nACTION PLAN\nName: {action_plan['action_plan']}\nDetails: {action_plan['details']}"

    messages = [
        system_message(create_the_action_plan_prompt()),
        user_message(user_msg),
    ]
    log.info("Running prompt create_the_action_plan_prompt")
    response = gpt_messages(messages=messages, in_json=True)
    log.info("\n*****\nAction Plan:")
    log.info(response)
    return response


def create_action_plan_summary(
    prereqs, action_plan, task_ouput, action_plan_name, all_action_plans
):
    log.info(f"Summarizing {action_plan}")
    summaries = get_existing_summaries(all_action_plans)
    if summaries:
        summaries = f"ACTION PLAN SUMMARIES:\n{summaries}"

    messages = [
        system_message(summarize_action_plan_prompt()),
        user_message(
            f"""{prereqs}\
{summaries}

ACTION PLAN
Name:{action_plan_name}
{action_plan}

OUTPUTS:
{task_ouput}"""
        ),
    ]

    log.info("Running prompt summarize_action_plan_prompt")
    response = gpt_messages(messages=messages, in_json=True)
    log.info(f"\n*****\Summary for {action_plan_name}:")
    log.info(response)
    log.info("\n\n")
    return json.loads(response)["summary"]
