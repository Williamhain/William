import os
import sys
import pos.cli.pos_cli
import pos.gui.pos_gui

def main():
	# You can run either a command-line interface (CLI) 
	# or a graphical user interface (GUI) to your blogging system.
	if len(sys.argv) != 2:
		print('ERROR: wrong number of arguments')
		print('\nCorrect Command usage:')
		print('python -m pos option')
		print('where option is either cli or gui')
		sys.exit()

	if sys.argv[1] == 'cli':
		pos.cli.pos_cli.main()
	elif sys.argv[1] == 'gui':
		pos.gui.pos_gui.main()
	else:
		print('ERROR: Wrong argument')
		print('\nCorrect Command usage:')
		print('python -m pos option')
		print('where option is either cli or gui')


if __name__ == '__main__':
	main()
