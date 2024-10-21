import os, textwrap

def write( dest ):
	os.makedirs( dest, exist_ok=True )
	with open( os.path.join( dest, 'README.md' ), 'w' ) as f:
		f.write( textwrap.dedent( '''\
			Every file in this directory is auto-generated by scripts in src/build_scripts during the normal build process.

			Attempting to manually modify any files in this directory will have no effect on the final build!
			'''))

if __name__ == '__main__':
	write( '.' )
elif __name__ == '__build__':
	write( outdir )