import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 2, // Virtual Users
    duration: '30s',
}

export function setup() {
    return oauth('miguel1', 'nacional')
}

const files = [
    'audio.ogg', 
    'audio16.mp3', 'audio22.mp3', 'audio29.mp3', 'audio8.ogg',
    'audio10.ogg', 'audio17.mp3', 'audio23.wav', 'audio3.mp3', 'audio9.ogg',
    'audio11.mp3', 'audio18.mp3', 'audio24.wav', 'audio30.mp3',
    'audio12.mp3', 'audio19.mp3', 'audio25.wav', 'audio4.mp3',
    'audio13.mp3', 'audio2.mp3', 'audio26.wav', 'audio5.wav',
    'audio14.mp3', 'audio20.mp3', 'audio27.mp3', 'audio6.mp3',
    'audio15.mp3', 'audio21.mp3', 'audio28.mp3', 'audio7.ogg'
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
    http.post('http://host.docker.internal:5001/api/tasks', data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
}