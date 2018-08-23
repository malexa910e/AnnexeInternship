Path=/home/ryax/playground_privacy/RGPDVersion#path to change

# --- container building --- #
buildManag: Dockerfile/Dockerfile.Managing
	docker build -t manag_image -f Dockerfile/Dockerfile.Managing -q .

buildInfo: Dockerfile/Dockerfile.Information
	docker build -t info_image -f Dockerfile/Dockerfile.Information -q .

buildDisplay: Dockerfile/Dockerfile.Display
	docker build -t display_image -f Dockerfile/Dockerfile.Display -q .

buildCompute: Dockerfile/Dockerfile.Compute
	docker build -t compute_image -f Dockerfile/Dockerfile.Compute -q .

buildEmit: Dockerfile/Dockerfile.Emit
	docker build -t emit_image -f Dockerfile/Dockerfile.Emit -q .

# --- container running --- #
alarm: buildDisplay buildCompute buildEmit
	docker run -d --rm --name DisplayAlarm --env "option=Alarm" --net host -e DISPLAY display_image
	docker run -d --rm --name ComputeAlarm --env "option=Alarm" compute_image
	docker run -d --rm --name EmitAlarm --env "movie=Video/Alarme.mp4" --env "option=Alarm" emit_image

present: buildDisplay buildCompute buildEmit
	docker run -d --rm --name DisplayPresent --env "option=Present" --net host -e DISPLAY display_image
	docker run -d --rm --name ComputePresent --env "option=Present" compute_image
	docker run -d --rm --name EmitPresent --env "movie=Video/Present.mp4" --env "option=Present" emit_image

leaving: buildDisplay buildCompute buildEmit
	docker run -d --rm --name DisplayLeaving --env "option=Leaving" --net host -e DISPLAY display_image
	docker run -d --rm --name ComputeLeaving  --env "option=Leaving"  compute_image
	docker run -d --rm --name EmitLeaving --env "movie=Video/Leaving.mp4"  --env "option=Leaving" emit_image

managing: buildManag
	docker run -it --rm --name ManagContainer manag_image

security: buildInfo
	docker run -it --rm --name SecuContainer -v /etc/localtime:/etc/localtime:ro --mount type=bind,source=$(Path)/Security,target=/home --net host -e DISPLAY info_image  /bin/sh -c "python3 home/message.py"

access: buildInfo
	docker run -it --rm --name AccessContainer -v /etc/localtime:/etc/localtime:ro --mount type=bind,source=$(Path)/AccessControl,target=/home --net host -e DISPLAY info_image  /bin/sh -c "python3 home/message.py"

schedule: buildInfo
	docker run -it --rm --name ScheduleContainer -v /etc/localtime:/etc/localtime:ro --mount type=bind,source=$(Path)/ScheduleControl,target=/home --net host -e DISPLAY info_image  /bin/sh -c "python3 home/message.py"
# --- container stopping --- #
stopAlarm:
	docker stop ComputeAlarm
	docker stop DisplayAlarm
	docker stop EmitAlarm

stopPresent:
	docker stop ComputePresent
	docker stop DisplayPresent
	docker stop EmitPresent

stopLeaving:
	docker stop ComputeLeaving
	docker stop DisplayLeaving
	docker stop EmitLeaving
