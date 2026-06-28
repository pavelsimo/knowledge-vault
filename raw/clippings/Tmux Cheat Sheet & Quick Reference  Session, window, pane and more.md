---
title: "Tmux Cheat Sheet & Quick Reference | Session, window, pane and more"
source: "https://tmuxcheatsheet.com/"
author:
published:
created: 2026-05-10
description: "Master tmux with the comprehensive cheat sheet: session management, examples, installation guide and more for the ultimate terminal multiplexer."
tags:
  - "clippings"
---
## Tmux Cheat Sheet & Quick Reference

## Sessions

$ tmux

$ tmux new

$ tmux new-session

: new

Start a new session

$ tmux new-session -A -s mysession

Start a new session or attach to an existing session named *mysession*

$ tmux new -s mysession

: new -s mysession

Start a new session with the name *mysession*

: kill-session

kill/delete the current session

$ tmux kill-ses -t mysession

$ tmux kill-session -t mysession

kill/delete session *mysession*

$ tmux kill-session -a

kill/delete all sessions but the current

$ tmux kill-session -a -t mysession

kill/delete all sessions but *mysession*

Ctrl + b $

Rename session

Ctrl + b d

Detach from session

: attach -d

Detach others on the session (Maximize window by detach other clients)

$ tmux ls

$ tmux list-sessions

Ctrl + b s

Show all sessions

$ tmux a

$ tmux at

$ tmux attach

$ tmux attach-session

Attach to last session

$ tmux a -t mysession

$ tmux at -t mysession

$ tmux attach -t mysession

$ tmux attach-session -t mysession

Attach to a session with the name *mysession*

Ctrl + b w

Session and Window Preview

Ctrl + b (

Move to previous session

Ctrl + b )

Move to next session

## Windows

$ tmux new -s mysession -n mywindow

start a new session with the name *mysession* and window *mywindow*

Ctrl + b c

Create window

Ctrl + b ,

Rename current window

Ctrl + b &

Close current window

Ctrl + b w

List windows

Ctrl + b p

Previous window

Ctrl + b n

Next window

Ctrl + b 0... 9

Switch/select window by number

Ctrl + b l

Toggle last active window

Ctrl + b <

Open window actions menu

: swap-window -s 2 -t 1

Reorder window, swap window number 2(src) and 1(dst)

: swap-window -t -1

Move current window to the left by one position

: move-window -s src\_ses:win -t target\_ses:win

: movew -s foo:0 -t bar:9

: movew -s 0:0 -t 1:9

Move window from source to target

: move-window -s src\_session:src\_window

: movew -s 0:9

Reposition window in the current session

: move-window -r

: movew -r

Renumber windows to remove gap in the sequence

## Panes

Ctrl + b ;

Toggle last active pane

: split-window -h

Ctrl + b %

Split the current pane with a vertical line to create a horizontal layout

: split-window -v

Ctrl + b "

Split the current with a horizontal line to create a vertical layout

: join-pane -s 2 -t 1

Join two windows as panes (Merge window 2 to window 1 as panes)

: join-pane -s 2.1 -t 1.0

Move pane from one window to another (Move pane 1 from window 2 to pane after 0 of window 1)

Ctrl + b {

Move the current pane left

Ctrl + b }

Move the current pane right

Ctrl + b Ctrl + b Ctrl + b Ctrl + b

Switch to pane to the direction

: setw synchronize-panes

Toggle synchronize-panes(send command to all panes)

Ctrl + b Spacebar

Toggle between pane layouts

Ctrl + b o

Switch to next pane

Ctrl + b q

Show pane numbers

Ctrl + b q 0... 9

Switch/select pane by number

Ctrl + b z

Toggle pane zoom

Ctrl + b !

Convert pane into a window

Ctrl + b + Ctrl + b Ctrl + Ctrl + b + Ctrl + b Ctrl +

Resize current pane height(holding second key is optional)

Ctrl + b + Ctrl + b Ctrl + Ctrl + b + Ctrl + b Ctrl +

Resize current pane width(holding second key is optional)

Ctrl + b x

Close current pane

Ctrl + b \>

Open pane actions menu

## Copy Mode

: setw -g mode-keys vi

use vi keys in buffer

Ctrl + b \[

Enter copy mode

Ctrl + b PgUp

Enter copy mode and scroll one page up

q

Quit mode

g

Go to top line

G

Go to bottom line

Scroll up

Scroll down

h

Move cursor left

j

Move cursor down

k

Move cursor up

l

Move cursor right

w

Move cursor forward one word at a time

b

Move cursor backward one word at a time

/

Search forward

?

Search backward

n

Next keyword occurance

N

Previous keyword occurance

Spacebar

Start selection

Esc

Clear selection

Enter

Copy selection

Ctrl + b \]

Paste contents of buffer\_0

: show-buffer

display buffer\_0 contents

: capture-pane

copy entire visible contents of pane to a buffer

: list-buffers

Show all buffers

: choose-buffer

Show all buffers and paste selected

: save-buffer buf.txt

Save buffer contents to *buf.txt*

: delete-buffer -b 1

delete buffer\_1

## Misc

Ctrl + b :

Enter command mode

: set -g OPTION

Set OPTION for all sessions

: setw -g OPTION

Set OPTION for all windows

: set mouse on

Enable mouse mode

$ tmux -V

Print tmux version

## Help

$ tmux list-keys

: list-keys

Ctrl + b ?

List key bindings(shortcuts)

$ tmux info

Show every session, window, pane, etc...