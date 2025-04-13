# Children's Castle - Interactive Storytime App

An engaging, mobile-friendly interactive storytime web application designed for young children, combining educational storytelling with comprehensive game-based learning experiences.

## Features

- Interactive storytelling with animated visuals
- Game-based learning experiences
- AI-powered voice narration via ElevenLabs
- Parent and child account system
- Comprehensive reward system
- Firebase authentication
- Responsive design for all devices
- OpenAI integration for AI assistant

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Firebase account
- OpenAI API key
- ElevenLabs API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   ```
   DATABASE_URL=your_database_url
   OPENAI_API_KEY=your_openai_key
   FIREBASE_API_KEY=your_firebase_key
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_APP_ID=your_app_id
   ELEVENLABS_API_KEY=your_elevenlabs_key
   ```
4. Initialize the database:
   ```
   python -c "from app import db; db.create_all()"
   ```
5. Start the application:
   ```
   python main.py
   ```

## Deployment Options

There are three main deployment options for Children's Castle:

### Option 1: Replit Deployment

The simplest option is to use Replit's built-in deployment:

1. Click the Deploy button in the Replit interface
2. Follow the prompts to deploy your application
3. Your app will be available at `https://your-project-name.replit.app`

See `REPLIT_VS_FIREBASE.md` for more details.

### Option 2: Firebase + Cloud Run Manual Deployment

For a more professional setup, deploy with Firebase Hosting and Cloud Run:

1. Run the deployment script:
   ```
   ./deploy_to_cloud_run.sh
   ```
2. Follow the prompts to configure your deployment
3. Your app will be available at `https://story-time-fun-1.web.app`

See `FULL_DEPLOYMENT_GUIDE.md` for detailed instructions.

### Option 3: GitHub Actions Automated Deployment (Recommended)

For continuous integration and deployment:

1. Push your code to GitHub repository: https://github.com/feysalh1/castle
2. GitHub Actions will automatically deploy to Firebase
3. Your app will be available at `https://story-time-fun-1.web.app` and `https://childrencastles.com`

This option requires:
- Firebase Service Account added to GitHub Secrets
- GitHub Actions workflow configured (already done in this repository)

See `FIREBASE_GITHUB_INTEGRATION.md` for detailed setup instructions.

## Custom Domain Setup

To connect your custom domain (childrencastles.com):

- For Replit: See `CUSTOM_DOMAIN_SETUP.md`
- For Firebase/Cloud Run: See `CUSTOM_DOMAIN_CLOUD_RUN.md`

## Technologies

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Authentication:** Firebase Auth, Flask-Login
- **Frontend:** HTML5, CSS3, JavaScript
- **AI Integration:** OpenAI GPT-4, ElevenLabs Voice API
- **Deployment:** Replit, Firebase Hosting, Google Cloud Run

## License

All rights reserved. This project is proprietary.

## Support

For support, contact the development team or submit an issue in the project repository.# Children's Castle
