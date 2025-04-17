#!/bin/bash

# 设置脚本所在目录为工作目录
cd "$(dirname "$0")"

uv run python main.py
