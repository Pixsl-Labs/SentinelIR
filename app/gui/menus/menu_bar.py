"""
Menu bar builder for the SentinelIR GUI.
"""

from app.gui.menus.file_menu import build_file_menu
from app.gui.menus.analysis_menu import build_analysis_menu
from app.gui.menus.detection_menu import build_detection_menu
from app.gui.menus.live_monitoring_menu import build_live_monitoring_menu
from app.gui.menus.generator_menu import build_generator_menu
from app.gui.menus.reports_menu import build_reports_menu
from app.gui.menus.settings_menu import build_settings_menu
from app.gui.menus.view_menu import build_view_menu
from app.gui.menus.help_menu import build_help_menu


def build_menu_bar(window) -> None:
    """
    Builds all GUI menus for the provided MainWindow instance.

    Args:
        window: MainWindow instance that owns the menu bar and callback methods.

    Returns:
        None
    """

    build_file_menu(window)
    build_analysis_menu(window)
    build_detection_menu(window)
    build_live_monitoring_menu(window)
    build_generator_menu(window)
    build_reports_menu(window)
    build_settings_menu(window)
    build_view_menu(window)
    build_help_menu(window)

# ============================================================
# Live Monitoring
# ============================================================

# Start Monitoring
# Stop Monitoring
# Select Watched File
# Add Watched File
# Remove Watched File
# View Live Summary

# Shortcuts:
# Ctrl+3 -> Live Monitoring screen
# F6 -> Start Monitoring
# Shift+F6 -> Stop Monitoring

# Icons:
# start / play
# stop
# log file
# add file
# remove file
# live dashboard


# ============================================================
# Generator
# ============================================================

# Generate Brute-force Scenario
# Generate Suspicious Success Scenario
# Generate User Targeting Scenario
# Generate Normal Activity
# Generate Mixed Attack
# Stream Scenario

# Shortcuts:
# Ctrl+4 -> Generator screen
# Ctrl+G -> Generate Scenario

# Icons:
# generate file
# cyber attack
# warning login
# target user
# normal activity
# streaming


# ============================================================
# Reports
# ============================================================

# Export TXT Report
# Export JSON Report
# Open Reports Folder
# Clear Reports

# Shortcuts:
# Ctrl+Shift+T -> Export TXT Report
# Ctrl+Shift+J -> Export JSON Report

# Icons:
# txt file
# json file
# open folder
# delete document
# report analytics


# ============================================================
# Terminal
# ============================================================

# Open Terminal
# Clear Terminal
# Run Last Command
# Custom Shortcuts

# Shortcuts:
# Ctrl+` -> Terminal
# Ctrl+L -> Clear Terminal

# Icons:
# terminal
# command line
# clear console
# keyboard shortcut


# ============================================================
# Settings
# ============================================================

# Detection Thresholds
# Live Monitoring Settings
# Watched Files
# Output Paths
# Reset Defaults

# Icons:
# settings gear
# threshold
# monitor settings
# watched folder
# output folder
# reset settings


# ============================================================
# View
# ============================================================

# Dashboard
# Static Analysis
# Live Monitoring
# Config
# Generator
# Terminal

# Shortcuts:
# Ctrl+1 -> Dashboard
# Ctrl+2 -> Static Analysis
# Ctrl+3 -> Live Monitoring
# Ctrl+4 -> Generator
# Ctrl+5 -> Config
# Ctrl+` -> Terminal

# Icons:
# dashboard
# analytics
# live data
# configuration
# generator
# terminal


# ============================================================
# Appearance
# ============================================================

# Light Mode
# Dark Mode
# System Default
# Toggle Theme

# Shortcut:
# Ctrl+Shift+D -> Toggle Dark Mode

# Icons:
# sun
# moon
# theme
# appearance


# ============================================================
# Help
# ============================================================

# User Guide
# Keyboard Shortcuts
# About SentinelIR

# Shortcuts:
# F1 -> User Guide
# Ctrl+/ -> Keyboard Shortcuts

# Icons:
# help
# keyboard shortcut
# information
# shield


# ============================================================
# Future GUI Ideas
# ============================================================

# Sidebar navigation
# Dashboard stat cards
# Recent alerts table
# Selected file status
# Current config summary
# Live monitoring status badge
# Theme toggle on far right
# Built-in terminal panel
# Report preview screen
# Export confirmation popup
# Error popup for missing files