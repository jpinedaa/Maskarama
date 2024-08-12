# Setup Instructions for Node.js, Git, and Next.js

This guide provides instructions for setting up Node.js, NVM (optional), Git, and running a Next.js app locally on both Windows and Linux systems.

## Windows Instructions

### 1. Install Node.js

1. Visit the official Node.js website: https://nodejs.org/
2. Download the LTS (Long Term Support) version for Windows.
3. Run the installer and follow the installation wizard.
4. To verify the installation, open Command Prompt and type:
   ```
   node --version
   npm --version
   ```

### 2. Install NVM for Windows (Optional)

1. Visit the NVM for Windows repository: https://github.com/coreybutler/nvm-windows
2. Download and run the latest nvm-setup.zip file.
3. Follow the installation wizard.
4. To verify the installation, open a new Command Prompt and type:
   ```
   nvm version
   ```

### 3. Install Git

1. Visit the official Git website: https://git-scm.com/download/win
2. Download the latest version for Windows.
3. Run the installer and follow the installation wizard.
4. To verify the installation, open Command Prompt and type:
   ```
   git --version
   ```

### 4. Clone the Repository and Run the Next.js App

1. Open Command Prompt.
2. Navigate to the directory where you want to clone the repository:
   ```
   cd path\to\your\directory
   ```
3. Clone the repository:
   ```
   git clone https://github.com/drshotyou/echoes-of-creation.git
   ```
4. Navigate into the cloned repository:
   ```
   cd echoes-of-creation
   ```
5. Install dependencies:
   ```
   npm install
   ```
6. Run the development server:
   ```
   npm run dev
   ```

## Linux Instructions

### 1. Install Node.js and NPM

You can install Node.js and NPM using your distribution's package manager or NVM.

Using package manager (Ubuntu/Debian example):
```
sudo apt update
sudo apt install nodejs npm
```

To verify the installation:
```
node --version
npm --version
```

### 2. Install NVM (Optional)

1. Open a terminal and run:
   ```
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
   ```
2. Close and reopen your terminal, or run:
   ```
   source ~/.bashrc
   ```
3. To verify the installation:
   ```
   nvm --version
   ```

### 3. Install Git

Most Linux distributions come with Git pre-installed. If not, you can install it using your package manager.

For Ubuntu/Debian:
```
sudo apt update
sudo apt install git
```

To verify the installation:
```
git --version
```

### 4. Clone the Repository and Run the Next.js App

1. Open a terminal.
2. Navigate to the directory where you want to clone the repository:
   ```
   cd /path/to/your/directory
   ```
3. Clone the repository:
   ```
   git clone <repository-url>
   ```
4. Navigate into the cloned repository:
   ```
   cd <repository-name>
   ```
5. Install dependencies:
   ```
   npm install
   ```
6. Run the development server:
   ```
   npm run dev
   ```

After following these steps, your Next.js app should be running locally. You can access it by opening a web browser and navigating to `http://localhost:3000`




###################################################################################################################################################################################################################
# Create T3 App

This is a [T3 Stack](https://create.t3.gg/) project bootstrapped with `create-t3-app`.

## What's next? How do I make an app with this?

We try to keep this project as simple as possible, so you can start with just the scaffolding we set up for you, and add additional things later when they become necessary.

If you are not familiar with the different technologies used in this project, please refer to the respective docs. If you still are in the wind, please join our [Discord](https://t3.gg/discord) and ask for help.

- [Next.js](https://nextjs.org)
- [NextAuth.js](https://next-auth.js.org)
- [Prisma](https://prisma.io)
- [Drizzle](https://orm.drizzle.team)
- [Tailwind CSS](https://tailwindcss.com)
- [tRPC](https://trpc.io)

## Learn More

To learn more about the [T3 Stack](https://create.t3.gg/), take a look at the following resources:

- [Documentation](https://create.t3.gg/)
- [Learn the T3 Stack](https://create.t3.gg/en/faq#what-learning-resources-are-currently-available) — Check out these awesome tutorials

You can check out the [create-t3-app GitHub repository](https://github.com/t3-oss/create-t3-app) — your feedback and contributions are welcome!

## How do I deploy this?

Follow our deployment guides for [Vercel](https://create.t3.gg/en/deployment/vercel), [Netlify](https://create.t3.gg/en/deployment/netlify) and [Docker](https://create.t3.gg/en/deployment/docker) for more information.
