import os, requests, json

step_cnt = 3
mode = 'deploy'
skip_build = True

port = 1044
docker_image = "voice-vector-web:latest"
marathon_id = "zeze.zzz/vv-web"
is_dev = True

if step_cnt > 0 and skip_build == False:
    print('[STEP 1/3] docker build...')
    os.system('docker build . -t idock.daumkakao.io/kakaobrain/{}'.format(docker_image))

if mode == 'run':
    if step_cnt > 1:
        print('[STEP 2/2] docker run...')
        os.system('docker run -p {}:{} idock.daumkakao.io/kakaobrain/{}'.format(port, port, docker_image))

if mode == 'deploy':
    if step_cnt > 1:
        print('[STEP 2/3] docker push...')
        os.system('docker push idock.daumkakao.io/kakaobrain/{}'.format(docker_image))

    if step_cnt > 2:
        print('[STEP 3/3] restart marathon instance...')
        if is_dev:
            marathon_api_url = "http://dcos.brain.dev.9rum.cc/marathon/v2/"
        else:
            marathon_api_url = "http://dcos.brain.9rum.cc/marathon/v2/"
        marathon_restart_url = "{}/apps/{}/restart?force=True".format(marathon_api_url, marathon_id)
        marathon_response = requests.post(marathon_restart_url)

        if marathon_response.status_code == 200:
            restart_deploy_id = json.loads(marathon_response.text)['deploymentId']
            print("Restart Success - deploy id : {}".format(restart_deploy_id))

        else:
            print('Restart Failed - STATUS {}'.format(marathon_response.status_code))