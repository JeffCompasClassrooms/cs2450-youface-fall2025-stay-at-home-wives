const glCanvas = document.getElementById("glCanvas");
const gl = glCanvas.getContext("webgl");

// --- Shaders ---
const vsSource = `
attribute vec2 aPosition;
attribute vec2 aUV;
varying vec2 vUV;
void main() {
    gl_Position = vec4(aPosition, 0.0, 1.0);
    vUV = aUV;
}
`;

const fsSource = `
precision mediump float;
uniform sampler2D uTexture;
varying vec2 vUV;
void main() {
    gl_FragColor = texture2D(uTexture, vUV);
}
`;

function compileShader(src, type) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS))
        throw new Error(gl.getShaderInfoLog(s));
    return s;
}

const vs = compileShader(vsSource, gl.VERTEX_SHADER);
const fs = compileShader(fsSource, gl.FRAGMENT_SHADER);

// Program
const program = gl.createProgram();
gl.attachShader(program, vs);
gl.attachShader(program, fs);
gl.linkProgram(program);
gl.useProgram(program);

// --- Geometry for full-screen quad ---
const positions = new Float32Array([
  -1,-1, 0,0,
   1,-1, 1,0,
  -1, 1, 0,1,
   1, 1, 1,1
]);
const buffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

const aPosition = gl.getAttribLocation(program, "aPosition");
const aUV = gl.getAttribLocation(program, "aUV");

gl.enableVertexAttribArray(aPosition);
gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 16, 0);

gl.enableVertexAttribArray(aUV);
gl.vertexAttribPointer(aUV, 2, gl.FLOAT, false, 16, 8);

// --- Texture ---
const canvas1 = document.getElementById("mapCanvas");
const tex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, tex);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas1);

// Uniform
const uTexture = gl.getUniformLocation(program, "uTexture");
gl.uniform1i(uTexture, 0); // texture unit 0

// --- Draw ---
gl.clearColor(0,0,0,1);
gl.clear(gl.COLOR_BUFFER_BIT);
gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
