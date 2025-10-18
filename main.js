const https = require('https');
const fs = require('fs');
const crypto = require('crypto');

let reqs = 0, success = 0, fails = 0;
let rps = 0, rpm = 0;

const devices = fs.existsSync('devices.txt') ? fs.readFileSync('devices.txt', 'utf-8').split('\n').filter(Boolean) : [];
const proxies = fs.existsSync('proxies.txt') ? fs.readFileSync('proxies.txt', 'utf-8').split('\n').filter(Boolean) : [];

// Simple input function without readline-sync
function getInput(question) {
    process.stdout.write(question);
    return new Promise((resolve) => {
        const stdin = process.stdin;
        stdin.resume();
        stdin.once('data', (data) => {
            resolve(data.toString().trim());
        });
    });
}

function gorgon(params, data, cookies, unix) {
    function md5(input) {
        return crypto.createHash('md5').update(input).digest('hex');
    }
    let baseStr = md5(params) + (data ? md5(data) : '0'.repeat(32)) + (cookies ? md5(cookies) : '0'.repeat(32));
    return {
        'X-Gorgon': '0404b0d300000000000000000000000000000000',
        'X-Khronos': unix.toString()
    };
}

function sendRequest(did, iid, cdid, openudid, aweme_id) {
    return new Promise((resolve) => {
        const params = `device_id=${did}&iid=${iid}&device_type=SM-G973N&app_name=musically_go&host_abi=armeabi-v7a&channel=googleplay&device_platform=android&version_code=160904&device_brand=samsung&os_version=9&aid=1340`;
        const payload = `item_id=${aweme_id}&play_delta=1`;
        const sig = gorgon(params, null, null, Math.floor(Date.now() / 1000));
        
        const options = {
            hostname: 'api16-va.tiktokv.com',
            port: 443,
            path: `/aweme/v1/aweme/stats/?${params}`,
            method: 'POST',
            headers: {
                'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                'x-gorgon': sig['X-Gorgon'],
                'x-khronos': sig['X-Khronos'],
                'user-agent': 'okhttp/3.10.0.1',
                'content-type': 'application/x-www-form-urlencoded',
                'content-length': Buffer.byteLength(payload)
            },
            timeout: 5000
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                reqs++;
                try {
                    const jsonData = JSON.parse(data);
                    if (jsonData && jsonData.log_pb && jsonData.log_pb.impr_id) {
                        success++;
                        console.log(`✅ Sent views ${jsonData.log_pb.impr_id} | reqs: ${reqs}`);
                    } else {
                        fails++;
                    }
                } catch (e) {
                    fails++;
                }
                resolve();
            });
        });

        req.on('error', (e) => {
            fails++;
            reqs++;
            resolve();
        });

        req.on('timeout', () => {
            req.destroy();
            fails++;
            reqs++;
            resolve();
        });

        req.write(payload);
        req.end();
    });
}

async function sendBatch(batchDevices, aweme_id) {
    const promises = batchDevices.map(device => {
        const [did, iid, cdid, openudid] = device.split(':');
        return sendRequest(did, iid, cdid, openudid, aweme_id);
    });
    await Promise.all(promises);
}

function statsLoop() {
    let lastReqs = reqs;
    setInterval(() => {
        rps = ((reqs - lastReqs) / 1.5).toFixed(1);
        rpm = (rps * 60).toFixed(1);
        lastReqs = reqs;
        process.title = `TikTok Viewbot | Success: ${success} | Fails: ${fails} | Reqs: ${reqs} | RPS: ${rps} | RPM: ${rpm}`;
    }, 1500);
}

function printBanner() {
    console.clear();
    console.log('\x1b[36m╔══════════════════════════════════════════════════════════════╗\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                              \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[35m╦  ╦╦╔═╗╦ ╦╔╗ ╔═╗╔╦╗  ╦ ╦╔═╗╦  ╔═╗╦ ╦╦╔═╗╔╗╔╔═╗  \x1b[0m  \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[35m╚╗╔╝║║╣ ║║║╠╩╗║ ║ ║   ║║║╠═╣║  ║ ║║║║║║ ║║║║║╣   \x1b[0m  \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m  \x1b[35m ╚╝ ╩╚═╝╚╩╝╚═╝╚═╝ ╩   ╚╩╝╩ ╩╩═╝╚═╝╚╩╝╩╚═╝╝╚╝╚═╝  \x1b[0m  \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                              \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m               \x1b[33mCREATED BY: NAIMUL HACKER KING\x1b[0m               \x1b[36m║\x1b[0m');
    console.log('\x1b[36m║\x1b[0m                                                              \x1b[36m║\x1b[0m');
    console.log('\x1b[36m╚══════════════════════════════════════════════════════════════╝\x1b[0m');
    console.log('');
}


async function main() {
    printBanner();
    
    console.log('\x1b[33m🚀 TikTok View Bot v3.0 - Ready!\x1b[0m\n');
    console.log('\x1b[36m📊 System Status:\x1b[0m');
    console.log(`   \x1b[36m• Devices Loaded: ${devices.length}\x1b[0m`);
    console.log(`   \x1b[36m• Proxies Loaded: ${proxies.length}\x1b[0m`);
    console.log('');
    



    // Get video link from command line arguments or ask for input
    let aweme_id;
    if (process.argv[2]) {
        const link = process.argv[2];
        const idMatch = link.match(/\d{18,19}/g);
        if (idMatch) {
            aweme_id = idMatch[0];
        }
    }

    if (!aweme_id) {
        console.log('Enter Video Link or ID:');
        const link = await getInput(' = ');
        const idMatch = link.match(/\d{18,19}/g);
        if (!idMatch) {
        console.log('\x1b[31m❌ Invalid video link or ID\x1b[0m');
        console.log('\x1b[33m💡 Please enter a valid TikTok video link or 18-19 digit ID\x1b[0m');
            process.exit(0);
        }
        aweme_id = idMatch[0];
    }

    if (devices.length === 0) {
        console.log('❌ devices.txt is empty or missing!');
        process.exit(1);
    }

    console.log(`\n\x1b[32m🎯 Target Video ID: ${aweme_id}\x1b[0m`);
    console.log('\x1b[33m🚀 Starting view bot... Press Ctrl+C to stop\x1b[0m');
    console.log('\x1b[33m⏳ Initializing...\x1b[0m\n');

    statsLoop();

    const concurrency = 200;

    while (true) {
        const batchDevices = [];
        for (let i = 0; i < concurrency && i < devices.length; i++) {
            batchDevices.push(devices[Math.floor(Math.random() * devices.length)]);
        }
        await sendBatch(batchDevices, aweme_id);
        
        await new Promise(resolve => setTimeout(resolve, 100));
    }
}

process.on('SIGINT', () => {
    console.log('\n\n🛑 Shutting down...');
    console.log(`📈 Final Stats:`);
    console.log(`   • Successful: ${success}`);
    console.log(`   • Failed: ${fails}`);
    console.log(`   • Total Requests: ${reqs}`);
    console.log(`\nThanks for using NAIMUL HACKER KING Viewbot! 👑`);
    process.exit(0);
});

// Run the script
main().catch(console.error);