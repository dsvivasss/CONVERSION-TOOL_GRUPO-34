import http from 'k6/http';

export function oauth () {
    const urlToken = 'http://34.136.168.9/api/auth/login'

    const data = {
        username: 'daniel',
        password: 'nacional'
    }

    const response = http.post(urlToken, JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return response.json('token')
}