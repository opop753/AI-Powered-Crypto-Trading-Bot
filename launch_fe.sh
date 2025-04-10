#!/bin/bash

# Terminal control sequences for clearing and moving cursor
clear_screen() {
    tput clear
}

move_to_bottom() {
    lines=$(tput lines)
    tput cup $((lines-2)) 0
}

# Kill frontend processes function
kill_frontend() {
    move_to_bottom
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🛑 Killing frontend processes..."
    pkill -f 'npm run'
    echo "✅ Done"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    tput cup $((lines-1)) 0
}

# Display menu at the bottom of the screen
display_menu() {
    move_to_bottom
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Options: [d]ev | [b]uild | [p]review | [s]torybook | build-[S]torybook | [k]ill | [q]uit"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Run commands with clear screen preparation
run_command() {
    clear_screen
    echo "🚀 Running: $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    eval "$1"
    echo ""
    display_menu
}

# Auto-run the development server at startup
clear_screen
echo "🚀 Auto-starting development server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
npm run dev &

while true; do
    display_menu
    read -n 1 -s key
    
    case $key in
        d)
            kill_frontend
            run_command "npm run dev" 
            ;;
        b)
            kill_frontend
            run_command "npm run build"
            ;;
        p)
            kill_frontend
            run_command "npm run preview"
            ;;
        s)
            kill_frontend
            run_command "npm run storybook"
            ;;
        S)
            kill_frontend
            run_command "npm run build-storybook"
            ;;
        k)
            kill_frontend
            ;;
        q)
            kill_frontend
            clear_screen
            echo "👋 Goodbye!"
            exit 0
            ;;
    esac
done
