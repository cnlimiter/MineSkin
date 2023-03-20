module.exports = {
    apps: [
        {
            name: 'mcskin',
            script: 'app.js',
            instances: 2,
            exec_mode: 'cluster',
            env: {
                NODE_ENV: 'production'
            }
        }
    ]
}
