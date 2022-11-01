import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 10, // Virtual Users
    duration: '2m',
}

export function setup() {
    return '23'
}

const files = [
    'audio5.wav', 'audio23.wav', 'audio24.wav', 'audio25.wav',
    'audio26.wav'
]
const dir = {}
files.forEach(elem => {
    dir[elem] = open(`/scripts/audios/${elem}`, 'b')
})
export default function (token) {
    const randomName = files[Math.floor(Math.random() * files.length)];
    const data = {
        newFormat: 'mp3',
        fileName: http.file(dir[randomName], randomName)
    };
    const res = http.post('http://34.136.168.9/api/tasks', data, {
        headers: {
            'Authorization': `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjcyODEyNzIsImV4cCI6MTY2NzI4NDg3Miwic3ViIjoiZGFuaWVsIiwiaXNzIjoid3d3LnRlc3QuY29tIn0.l45c7e1OIeHPFRKS0JaCiHryvIkNXW8pu73dimCJhfU`
        }
    });
    if(res.status != 200){
        console.log(res.body)
    }
}