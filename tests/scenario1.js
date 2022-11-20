import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 10, // Virtual Users
    duration: '30s',
}

export function setup() {
    return '23'
}

const files = [
    'audio5.ogg',
    'audio23.ogg',
    'audio24.ogg',
    'audio25.ogg',
    'audio26.ogg'
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
    const res = http.post('http://host.docker.internal:5000/api/tasks', data, {
        headers: {
            'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Njg5NzU1NDIsImV4cCI6MTY2ODk3OTE0Miwic3ViIjoiaXNtYWVsIiwiaXNzIjoid3d3LnRlc3QuY29tIn0.tGqflBv6AMv27JvzObe0bOqXFWgZ8m2x93l0UsnBo2Y`
        }
    });
    if(res.status != 200){
        console.log(res.body)
    }
}