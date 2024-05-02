import argparse
import json
from dotenv import load_dotenv
from app.gpt import gpt_messages

# from app.prompts.convert_repo import (
#     action_plan_prompt,
#     perform_the_action_prompt,
# )
from app.prompts.create_project import (
    initial_assessment_prompt,
    define_action_plan_prompt,
)
from app.messages import system_message, user_message
from app.tools.runner import (
    run_tool,
    run_tools,
    get_prerequisites,
    create_detailed_action_plan,
    create_action_plan_summary,
)
from app.utils.file_system import empty_directory
from app.utils.logger import setup_logger

log = setup_logger()
load_dotenv()

parser = argparse.ArgumentParser(
    description="List files in a directory in hierarchical format."
)
parser.add_argument("path", type=str, help="The root directory path")

args = parser.parse_args()


def remove_system_message(messages):
    messages.pop(0)


def doit():
    # delete_subfolder(args.path, "target")
    # delete_subfolder(args.path, "venv")
    # folder_struct = get_folder_inventory(args.path)
    empty_directory(args.path)
    messages = [
        # system_message(action_plan_prompt()),
        # user_message(f"Here's my repo's folder structure:\n\n{folder_struct}"),
        system_message(initial_assessment_prompt()),
        user_message(
            """I want you to create me an app that will be used to help the user share their \
dietary preferences with their friend family. I call this app Dan's Diet. The primary user base \
are those creating diets, whether for themselves or their family members, i.e. a mom creating one \
for their kids.

Here's how it works:
As a user managing a diet:
- I can create a diet and name it, I could have more than one to manage.
- I can select from a predefined diet like Low FODMAP, Gluten-Free, Dairy Free, etc.
- Within a diet, I can select which foods are restricted, along with possible substituions.
- I can also add foods that are allowed.
- The app should automatically create a header image using the GenAI image service, DALLE-3.
- I can share my diet using a simple share link.

As a user viewing a shared diet:
- I will see the hero image and name of the diet.
- I will see all of the restricted foods first, then the allowed foods.
- If a restricted food has a substitution, I will see it in the same card as the restricted food.

As an admin to the app:
- I can view all of the users in the app, the date and time they last logged in, and how many diets they have
- I can manage the user account individually by resetting their password, or disabling their account
- I can view adoption stats of my app in simple reports, like total number of users, total number of diets, average diets \
per person, total shares viewed, average share views per user, etc.

Technical requirements:
- The entire stack will be hosted in AWS, use AWS Amplify for the frontend and backend
    - Backend should be written in Python, ideally as Lambdas
    - Frontend should be written in ReactJS, create the app using create-react-app
    - The data should be stored in a relational database
- Aim for low cost, performance isn't incredibly important right now as it'll be a couple of users

Design requirements:
- The primary color should be a deep calm purple, you may identify secondary and tertiary colors
- Use a well known design framework and component library like Bootstrap or MaterialUI
- Build it mobile first
"""
        ),
    ]
    log.info("Running prompt initial_assessment_prompt")
    # response = gpt_messages(messages=messages, in_json=True)
    # response = gpt_messages(messages=messages)
    response = """'### Understanding the Intent for the Application

**Dan\'s Diet** aims to simplify the process of sharing dietary preferences and restrictions within personal circles, primarily targeting individuals responsible for managing diets for themselves or others (e.g., parents for their children). It emphasizes ease of creating, managing, and sharing diet plans with a focus on inclusivity regarding various dietary needs.

### Key Personas

1. **Diet Managers**: Individuals creating and managing diets. This includes people with specific dietary needs (due to health conditions, allergies, etc.) and those managing diets for others, like a parent for their child.

2. **Diet Viewers**: Friends and family members who receive shared diet plans. This group benefits from understanding the dietary restrictions and preferences of the Diet Managers to accommodate their needs in shared meals or events.

3. **Admins**: Users with the ability to oversee the application\'s user base, manage accounts, and view app adoption statistics to ensure smooth operation and user support.

### Key User Journeys

1. **Creating and Managing a Diet**:
   - User logs in/registers.
   - User creates a new diet, selects from predefined options or customizes it by adding restricted and allowed foods, along with substitutions.
   - User shares the diet via a link.

2. **Viewing a Shared Diet**:
   - User receives a share link and views the diet, including restrictions, allowed foods, and substitutions.

3. **Admin Management**:
   - Admin logs in.
   - Admin views user activity, manages accounts, and accesses app adoption statistics.

### Design Theme

- **Primary Color**: Deep calm purple
- **Secondary Color**: Light grey for backgrounds and cards to ensure readability and contrast.
- **Tertiary Color**: Soft green for buttons and interactive elements to signify action and positivity, complementing the primary purple.

### Ideal Tech Stack

- **Frontend**: ReactJS with Material-UI for a modern, responsive design that adheres to the mobile-first approach. Material-UI offers components that can easily be themed with the primary deep calm purple and other colors.

- **Backend**: Python with AWS Lambda for serverless backend logic, offering scalability and cost-efficiency. This aligns with the low-cost, performance-considerate requirement.

- **Database**: AWS RDS (Relational Database Service) with a PostgreSQL engine, providing a robust, scalable, and cost-effective relational database solution.

- **Hosting/Infrastructure**: AWS Amplify for frontend hosting and CI/CD, integrated with other AWS services (Lambda, RDS) for a cohesive and streamlined AWS-centric solution.

- **Image Generation**: Integration with DALL-E 3 API for automatic header image creation based on the diet\'s name and restrictions.

### Additional Considerations

- **Security**: Implement robust authentication and authorization mechanisms, especially for admin functionalities. Consider using AWS Cognito for user management and authentication.

- **Analytics**: Utilize AWS QuickSight or a similar tool for generating the adoption stats and reports required by admins.

- **Accessibility**: Ensure the app is accessible, following WCAG guidelines to accommodate users with disabilities.

This comprehensive approach aims to cover the functional, technical, and design aspects of "Dan\'s Diet," providing a clear roadmap for development that aligns with the user\'s vision and requirements.'"""

    requirements = response
    messages = [system_message(define_action_plan_prompt()), user_message(response)]
    response = """{
  "action_plans": [
    {
      "action_plan": "Project Setup and Initial Configuration",
      "details": "Create the initial project structure for both frontend and backend. Setup ReactJS project with Material-UI for the frontend, and initialize a Python project for AWS Lambda functions. Configure AWS Amplify for hosting and CI/CD integration.",
      "order": 1
    },
    {
      "action_plan": "Design System Implementation",
      "details": "Implement the design theme using Material-UI in the ReactJS project. Define global styles, themes, and component overrides using the primary, secondary, and tertiary colors. Ensure mobile-first and accessible design principles are applied.",
      "order": 2
    },
    {
      "action_plan": "Authentication and Authorization Setup",
      "details": "Integrate AWS Cognito for user management and authentication. Setup roles and permissions for Diet Managers, Diet Viewers, and Admins, ensuring secure access control for different parts of the application.",
      "order": 3
    },
    {
      "action_plan": "Database Design and Integration",
      "details": "Design the database schema for managing users, diet plans, food restrictions, and substitutions. Setup AWS RDS with PostgreSQL, and integrate it with the backend Lambda functions.",
      "order": 4
    },
    {
      "action_plan": "Backend API Development",
      "details": "Develop serverless backend APIs using AWS Lambda for user registration/login, creating and managing diet plans, sharing diets, and admin functionalities. Ensure APIs are secure and scalable.",
      "order": 5
    },
    {
      "action_plan": "Frontend Development for User Journeys",
      "details": "Implement the user interfaces for the key user journeys: creating and managing a diet, viewing a shared diet, and admin management. Use ReactJS and Material-UI, ensuring responsive and accessible design.",
      "order": 6
    },
    {
      "action_plan": "Integration with DALL-E 3 API",
      "details": "Integrate the DALL-E 3 API to automatically generate header images for diet plans based on the diet's name and restrictions. Ensure the integration is seamless and images are appropriately displayed in the UI.",
      "order": 7
    },
    {
      "action_plan": "Analytics and Reporting Setup",
      "details": "Integrate AWS QuickSight or a similar tool for generating adoption stats and reports for admin users. Setup necessary metrics and ensure data is accurately represented.",
      "order": 8
    },
    {
      "action_plan": "Testing and Quality Assurance",
      "details": "Conduct thorough testing across all components of the application. Include unit tests, integration tests, and user acceptance testing (UAT) to ensure functionality, security, and usability standards are met.",
      "order": 9
    },
    {
      "action_plan": "Launch and Continuous Improvement",
      "details": "Prepare for the application launch by ensuring all components are fully integrated and tested. Post-launch, continuously monitor, gather user feedback, and iterate on the application to improve features and performance.",
      "order": 10
    }
  ]
}"""
    log.info("Running prompt define_action_plan_prompt")
    response = """{
      "action_plans": [
        {
          "action_plan": "Project Setup and Initial Configuration",
          "details": "Set up the project repository, define the directory structure, and configure initial settings for ReactJS frontend and AWS backend services. Include setup for AWS Lambda, RDS with PostgreSQL, AWS Amplify, and Cognito for authentication. Establish CI/CD pipelines using AWS Amplify.",
          "order": 1
        },
        {
          "action_plan": "Design System and Theme Implementation",
          "details": "Develop a design system based on the provided color scheme (deep calm purple, light grey, soft green) using Material-UI. This includes creating a theme file, defining global styles, and ensuring accessibility standards are met.",
          "order": 2
        },
        {
          "action_plan": "Authentication and Authorization",
          "details": "Implement authentication and authorization mechanisms using AWS Cognito. Set up user roles (Diet Managers, Diet Viewers, Admins) with appropriate access controls.",
          "order": 3
        },
        {
          "action_plan": "Database Schema Design",
          "details": "Design and implement the database schema in AWS RDS PostgreSQL. This includes tables for users, diets, food restrictions, allowed foods, substitutions, and shared diet links.",
          "order": 4
        },
        {
          "action_plan": "Backend API Development",
          "details": "Develop RESTful APIs using AWS Lambda for user registration/login, diet management (creation, update, deletion), diet sharing, and admin functionalities (user activity monitoring, account management, app adoption statistics).",
          "order": 5
        },
        {
          "action_plan": "Frontend Development - User Registration and Login",
          "details": "Implement the user interface for registration and login processes, integrating with AWS Cognito for authentication.",
          "order": 6
        },
        {
          "action_plan": "Frontend Development - Diet Management",
          "details": "Develop the UI components and pages for creating, managing, and sharing diets. This includes forms for diet creation, listing diets, and a detailed view for each diet with options to edit, delete, or share.",
          "order": 7
        },
        {
          "action_plan": "Frontend Development - Viewing Shared Diets",
          "details": "Implement the UI for viewing shared diets through a shared link. Ensure viewers can see restrictions, allowed foods, and substitutions without needing to log in.",
          "order": 8
        },
        {
          "action_plan": "Admin Interface Development",
          "details": "Develop the admin interface for user activity monitoring, account management, and viewing app adoption statistics. Integrate with AWS QuickSight for analytics.",
          "order": 9
        },
        {
          "action_plan": "Integration with DALL-E 3 API",
          "details": "Implement the integration with DALL-E 3 API for generating header images for diets based on their names and restrictions. This involves calling the API from the backend and storing image references in the database.",
          "order": 10
        },
        {
          "action_plan": "Testing and Quality Assurance",
          "details": "Conduct thorough testing across all features and user journeys. This includes unit tests, integration tests, and user acceptance testing (UAT) to ensure functionality, performance, security, and accessibility standards are met.",
          "order": 11
        },
        {
          "action_plan": "Deployment and Monitoring",
          "details": "Deploy the application using AWS Amplify. Set up monitoring and logging with AWS CloudWatch to track application health and user activities. Prepare for continuous deployment and updates based on user feedback.",
          "order": 12
        }
      ]
    }"""
    # response = gpt_messages(messages=messages, in_json=True)
    log.info(f"\n*****\nAction Plans:\n\n{response}")
    action_plans = json.loads(response)["action_plans"]
    action_plans = sorted(action_plans, key=lambda task: task["order"])
    current_step = int(action_plans[0]["order"])
    last_step = int(action_plans[-1]["order"])
    prefix = f"""REQUIREMENTS:
{requirements}

HIGH LEVEL ACTION PLANS:
{response}\n\n"""
    while current_step <= last_step:
        for task in [task for task in action_plans if task["order"] == current_step]:
            prereqs = ""  # get_prerequisites(task, prefix, action_plans, args.path)
            action_plan_details = create_detailed_action_plan(
                task, prefix, prereqs, action_plans
            )
            task["action_plan_details"] = json.loads(action_plan_details)
            task_output = run_tools(task["action_plan_details"]["actions"], args.path)

            summary = create_action_plan_summary(
                prefix,
                action_plan_details,
                task_output,
                task["action_plan"],
                action_plans,
            )
            task["summary"] = summary
        current_step += 1
    return


if __name__ == "__main__":
    doit()
