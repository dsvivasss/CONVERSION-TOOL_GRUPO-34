import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 5, // Virtual Users
    duration: '1m',
}

export function setup() {
    return '23'
}

const files = [
    'audio5.mp3', 'audio23.mp3', 'audio24.mp3', 'audio25.mp3',
    'audio26.mp3'
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
    const res = http.post('http://34.150.214.140:5001/api/tasks', data, {
        headers: {
            'Authorization': `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2Njg0OTQyMzQsImV4cCI6MTY2ODQ5NzgzNCwic3ViIjoiaXNtYWVsIiwiaXNzIjoid3d3LnRlc3QuY29tIn0.84CjFDlHQ06w6KFg99oUQ_zV5c4lVg4YzA-vyxZDVlY`
        }
    });
    if(res.status != 200){
        console.log(res.body)
    }
}