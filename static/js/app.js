// Tampoco hay banderas en el JavaScript! ;)
particlesJS("particles-js", {
    "particles": {
        "number": {
            "value": 30,  
            "density": {
                "enable": true,
                "value_area": 800
            }
        },
        "color": {
            "value": "#ffffff"
        },
        "shape": {
            "type": "circle",
            "stroke": {
                "width": 0,
                "color": "#000000"
            }
        },
        "opacity": {
            "value": 0.5,  
            "random": false
        },
        "size": {
            "value": 2,  
            "random": true
        },
        "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.2,
            "width": 1
        },
        "move": {
            "enable": true,
            "speed": 2,  
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": false
        }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": {
                "enable": true,
                "mode": "repulse"
            },
            "onclick": {
                "enable": true,
                "mode": "push"
            },
            "resize": true
        },
        "modes": {
            "repulse": {
                "distance": 200,
                "duration": 0.4
            },
            "push": {
                "particles_nb": 4
            }
        }
    },
    "retina_detect": true
});

document.addEventListener('DOMContentLoaded', function() {
    // Cargar la hoja de estilo de forma asíncrona
    var stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = '/static/style.css';
    stylesheet.onload = function() {
        console.log('Hoja de estilo cargada exitosamente.');
    };
    document.head.appendChild(stylesheet);

    // Inicializar particles.js si está disponible
    if (typeof particlesJS !== 'undefined') {
        particlesJS.load('particles-js', '/static/particles.json', function() {
            console.log('Particles.js configurado exitosamente.');
        });
    } else {
        console.error('particlesJS no está definido.');
    }
});
