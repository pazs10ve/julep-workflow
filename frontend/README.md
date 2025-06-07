# Foodie Tour Frontend

This directory contains a React application that serves as the frontend for the AI Foodie Tour Planner.

## Prerequisites

Make sure you have [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) (or [Yarn](https://yarnpkg.com/)) installed.

## Available Scripts

In the `frontend` directory, you can run:

### `npm install` (or `yarn install`)

Installs all the necessary dependencies for the project.

### `npm start` (or `yarn start`)

Runs the app in development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.
You may also see any lint errors in the console.

**Note:** Ensure your FastAPI backend (from the parent directory's `app.py`) is running, typically on `http://localhost:8000`, for the frontend to fetch data.

### `npm test` (or `yarn test`)

Launches the test runner in interactive watch mode.

### `npm run build` (or `yarn build`)

Builds the app for production to the `build` folder.
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.
Your app is ready to be deployed!

## Connecting to the Backend

The frontend is configured to connect to the FastAPI backend at `http://localhost:8000`. If your backend runs on a different port, you'll need to update the `API_BASE_URL` constant in `src/App.js`.

## `.gitignore`

A standard `.gitignore` file for Create React App projects should be included here. 

Create a file named `.gitignore` in this `frontend` directory and add the following content to ensure `node_modules` and other build artifacts are not committed to version control:

```
# Dependencies
/node_modules
/.pnp
.pnp.js

# Testing
/coverage

# Production
/build

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
```
