#!/usr/bin/env bash


mv ~/.zsh_history{,_bad}
strings ~/.zsh_history_bad > ~/.zsh_history
fc -R ~/.zsh_history
rm ~/.zsh_history_bad
