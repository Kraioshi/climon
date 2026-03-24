# Mongoeb 
A simple lightweight CLI tool to quickly explore MongoDB-compatible databases (like Document DB) using simple commands instead of queries.

## Why?

I am lazy. 
Mongoeb allows:
- quickly inspect collections
- run simple queries
- explore data without boilerplate

## Features

### Currently read only.
- find documents with filters
- show collections
- count documents
- interactive shell mode
- simple CLI syntax (No JSON needed)

## Installation

### Option 1: pipx

```bash
pipx install git+https://github.com/Kraioshi/climon.git@v0.1.1
```

### Option 2: Standalone binary

Download appropriate file from the releases

### ⚠️ macOS / Linux
After downloading, you might need to make file executable:
```bash
chmod +x mongoeb-*
```
### macOS only (if still blocked)
```bash
xattr -d com.apple.quarantine mongoeb-*
```

## First-time setup

Run: 
```bash
mongoeb gazuyem
```
or 
```bash
mongoeb init
```

And follow the prompts

## Interactive shell

Start the shell:

```bash
mongoeb shell
```

Then type 
```bash
help
```
to see availabl commands
