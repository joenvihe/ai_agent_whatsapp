const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fetch = require('node-fetch'); // Asegúrate de instalar esta librería

// const client = new Client();
const client = new Client({
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});


client.on('qr', qr => {
    // Generar el código QR en la terminal para escanear con WhatsApp
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Client is ready!');
});

//client.on('message_create', message => {
client.on('message_create', async (message) => {
    console.log(`Mensaje recibido: ${message.body}`);

    try {
        const chat = await message.getChat(); // Obtener el chat relacionado al mensaje
        console.log(`Nombre del chat: ${chat.name}`);
        console.log(`Tipo de chat: ${chat.isGroup ? 'Grupo' : 'Individual'}`);
        console.log(`Cantidad de participantes: ${chat.participants ? chat.participants.length : 'N/A'}`);
    } catch (error) {
        console.error('Error al obtener el chat:', error);
    }

    try {
        const contact = await message.getContact(); // Obtener el contacto relacionado al mensaje
        console.log(`Nombre del contacto: ${contact.pushname}`);
        console.log(`Número de teléfono: ${contact.number}`);
        console.log(`ID del contacto: ${contact.id._serialized}`);
    } catch (error) {
        console.error('Error al obtener el contacto:', error);
    }

    const clientInfo = client.info;
    // Mostrar detalles básicos del cliente
    console.log(`Nombre: ${clientInfo.pushname}`);
    console.log(`Número: ${clientInfo.wid.user}`);
    console.log(`Plataforma: ${clientInfo.platform}`);

    // Si quieres que el bot pase el mensaje al API
    if (message.body.startsWith('!ask ')) {
        const question = message.body.replace('!ask ', '');

        try {
            // Llamar al API del contenedor "my-openai-api"
            const response = await fetch('http://my-openai-api:5000/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) throw new Error(`Error en la API: ${response.statusText}`);

            const data = await response.json();
            const answer = data.answer || 'Lo siento, no pude procesar la solicitud.';

            // Responder en WhatsApp
            await message.reply(answer);
        } catch (error) {
            console.error('Error al llamar a la API:', error);
            await message.reply('Hubo un error al procesar tu solicitud.');
        }
    }

    // Si quieres que el bot pase el mensaje al API
    if (message.body.startsWith('!cal ')) {
        const question = message.body.replace('!cal ', '');

        try {
            // Llamar al API del contenedor "my-openai-api"
            const response = await fetch('http://my-openai-api:5000/cal', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) throw new Error(`Error en la API: ${response.statusText}`);

            const data = await response.json();
            const answer = data.answer || 'Lo siento, no pude procesar la solicitud.';

            // Responder en WhatsApp
            await message.reply(answer);
        } catch (error) {
            console.error('Error al llamar a la API:', error);
            await message.reply('Hubo un error al procesar tu solicitud.');
        }
    }


    // Responder a un comando simple
    if (message.body === '!ping') {
        message.reply('pong');
    }
});

client.initialize();
