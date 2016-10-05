# Initialize world canvas

l_canvas = document.getElementById "life"
l_context = l_canvas.getContext "2d"

l_context.fillStyle = "rgba(0, 0, 0,0.1)"
l_context.fillRect 0, 0, 1220, 620
speed = 300

refresher = null
living = null

world =
	for x in [0..60]
		for y in [0..30]
			randomnum = 0
			!!randomnum
life =
	for x in [0..60]
		for y in [0..30]
			num = 1
			!!num

runvisualization = ->


	# Initialize a 2d array
	# False represents a "dead" cell, while true represents a "live" cell


	# Paint the initial world state
	drawworld = ->
		for x in [0..60]
			for y in [0..30]
				if world[x][y] == true
					switch life[x][y]
					 when 1 then l_context.fillStyle = "#1E90FF"
					 when 2 then l_context.fillStyle = "#008000"
					 when 3 then l_context.fillStyle = "red"
					 else l_context.fillStyle = "#1E90FF"
				else
					l_context.fillStyle = "#fff"

				l_context.fillRect x*20 + 2, y*20 + 2, 20 - 4, 20 - 4

	drawworld()

	getPosition = (event) ->
		x = event.x
		x-=7
		y = event.y
		y-=7

		x-= l_canvas.offsetLeft
		y-= l_canvas.offsetTop

		x/=20
		y/=20

		x = Math.round x
		y = Math.round y

		if world[x][y] then world[x][y] = false else world[x][y] = true
		if world[x][y] then life[x][y] = 1 else life[x][y] = 0



		drawworld()

	countneighbors = (x,y) ->
		total = 0

		if x == 0 then westindex = 60
		else westindex = x - 1

		if x == 60 then eastindex = 0
		else eastindex = x + 1

		if y == 0 then northindex = 30
		else northindex = y - 1

		if y == 30 then southindex = 0
		else southindex = y + 1

		if world[westindex][northindex] == true then total++
		if world[x][northindex]         == true then total++
		if world[eastindex][northindex] == true then total++
		if world[westindex][y]          == true then total++
		if world[eastindex][y]          == true then total++
		if world[westindex][southindex] == true then total++
		if world[x][southindex]         == true then total++
		if world[eastindex][southindex] == true then total++

		total

	incrementworld = ->
		# Deep copy of the world state
		newworld =
			for x in [0..60]
				for y in [0..30]
					world[x][y]

		newlife =
			for x in [0..60]
				for y in [0..30]
					life[x][y]

		for x in [0..60]
			for y in [0..30]
				neighbors = countneighbors x, y

				if world[x][y] == true
					if neighbors == 2 or neighbors == 3
						newworld[x][y] = true
						newlife[x][y]++
					else
						newworld[x][y] = false
						newlife[x][y] = 0
				else
					if neighbors == 3
						newworld[x][y] = true
						newlife[x][y] = 1

		# Update world with deep copy of new state
		world =
			for x in [0..60]
				for y in [0..30]
					newworld[x][y]
		life =
			for x in [0..60]
				for y in [0..30]
					newlife[x][y]

	stepforward = ->
		l_canvas.addEventListener "mousedown", getPosition, false
		drawworld()
		console.log speed
		if living == true
			incrementworld()
		drawworld()
		checkdead()

	checkdead = ->
		tot = 0
		for x in [0..60]
			for y in [0..30]
				if world[x][y] then tot++
		console.log tot
		if tot == 0 then setliving false


	refresher = setInterval stepforward, speed

runvisualization()

setliving = (val)->
	living = val

clearworld = ->
	world =
		for x in [0..60]
			for y in [0..30]
				randomnum = 0
				!!randomnum
	life =
		for x in [0..60]
			for y in [0..30]
				num = 0
				!!num
	console.log world
	setliving false

initrand = ->
	world =
		for x in [0..60]
			for y in [0..30]
				randomnum = Math.floor(Math.random() * 2)
				!!randomnum
	life =
		for x in [0..60]
			for y in [0..30]
				num = 1
				!!num

playbutton = document.getElementById 'start'
playbutton.onclick = -> setliving true

stopbutton = document.getElementById 'stop'
stopbutton.onclick = -> setliving false

restartbutton = document.getElementById 'restart'
restartbutton.onclick = -> clearworld()

randbutton = document.getElementById 'rand'
randbutton.onclick = -> initrand()
