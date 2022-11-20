import http from 'k6/http';

export function oauth () {
    const urlToken = 'http://host.docker.internal:5001/api/auth/login'

    const data = {
        username: 'miguel1',
        password: 'nacional'
    }

    const response = http.post(urlToken, JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return response.json('token')
}