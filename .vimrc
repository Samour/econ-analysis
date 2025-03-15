nmap cl :below ter ++rows=10 black %<CR>
nmap ct :below ter ++rows=10 mypy --strict %<CR>
command Py :below ter ++rows=15 ++close python3
nmap tt :below ter ++rows=15 python3 -m unittest %<CR>
