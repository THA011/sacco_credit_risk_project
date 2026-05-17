#!/bin/bash
# SACCO Credit Risk Project - Automated GitHub Push Script
# This script completes the setup and pushes the project to GitHub

echo "=========================================="
echo "SACCO Credit Risk Project - GitHub Push"
echo "=========================================="
echo ""

# Set your GitHub credentials here
GITHUB_USERNAME="YOUR_GITHUB_USERNAME"
GITHUB_EMAIL="your.email@example.com"

# Change to project directory
cd "C:\Users\Admin\Downloads\sacco_credit_risk_project" || {
    echo "ERROR: Could not find project directory"
    exit 1
}

echo "✓ Project directory confirmed"

# Configure git user
git config user.name "Mwatha Maina"
git config user.email "$GITHUB_EMAIL"
echo "✓ Git user configured"

# Verify local repo status
echo ""
echo "Local git status:"
git log --oneline -5
echo ""

# Add GitHub remote
echo "Adding GitHub remote..."
git remote add origin "https://github.com/${GITHUB_USERNAME}/sacco_credit_risk_project.git" 2>/dev/null || {
    echo "Remote may already exist, skipping..."
}

echo "✓ GitHub remote configured"

# Display push command
echo ""
echo "=========================================="
echo "READY TO PUSH TO GITHUB"
echo "=========================================="
echo ""
echo "Step 1: Create empty repository on GitHub"
echo "   Go to: https://github.com/new"
echo "   Name: sacco_credit_risk_project"
echo "   Do NOT initialize with README/gitignore"
echo ""
echo "Step 2: Push with this command:"
echo ""
echo "   git push -u origin master"
echo ""
echo "Step 3: When prompted for password, use a Personal Access Token (PAT)"
echo "   Get token from: https://github.com/settings/tokens"
echo "=========================================="
