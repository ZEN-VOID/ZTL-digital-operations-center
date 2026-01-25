/**
 * Embedded Divider Animation
 *
 * 轻量级p5.js动画，用于section过渡
 * 移除了UI控制面板，专注于核心动画效果
 *
 * 使用方法:
 * new EmbeddedDivider('canvas-id', {
 *   height: 60,
 *   particleCount: 15,
 *   accentColor: '#00BFFF'
 * });
 */

class EmbeddedDivider {
    constructor(containerId, userConfig = {}) {
        // 默认配置
        this.config = {
            width: 0,  // 自动从容器获取
            height: 60,
            particleCount: 15,
            flowSpeed: 1.0,
            trailLength: 8,
            waveAmplitude: 20,
            waveFrequency: 1.2,
            accentColor: '#00BFFF',
            showAttractors: false,  // 隐藏吸引点
            seed: 54321,
            backgroundAlpha: 15,  // 背景透明度 (用于拖尾效果)
            ...userConfig
        };

        this.containerId = containerId;
        this.particles = [];
        this.attractors = [];
        this.timeOffset = 0;
        this.p5Instance = null;

        this.init();
    }

    init() {
        const self = this;

        // 创建p5.js实例
        const sketch = (p) => {
            p.setup = () => {
                // 获取容器宽度
                const container = document.getElementById(self.containerId);
                const width = container ? container.offsetWidth : window.innerWidth;
                self.config.width = width;

                // 创建canvas
                const canvas = p.createCanvas(self.config.width, self.config.height);
                canvas.parent(self.containerId);

                // 初始化系统
                self.initializeSystem(p);
            };

            p.draw = () => {
                self.draw(p);
            };

            p.windowResized = () => {
                const container = document.getElementById(self.containerId);
                const width = container ? container.offsetWidth : window.innerWidth;
                self.config.width = width;
                p.resizeCanvas(width, self.config.height);
                self.initializeSystem(p);
            };
        };

        this.p5Instance = new p5(sketch);
    }

    initializeSystem(p) {
        p.randomSeed(this.config.seed);
        p.noiseSeed(this.config.seed);

        this.particles = [];
        this.attractors = [];

        // 创建8个吸引点横向排列
        for (let i = 0; i < 8; i++) {
            const x = p.map(i, 0, 7, this.config.width * 0.1, this.config.width * 0.9);
            const y = this.config.height / 2;
            this.attractors.push({
                pos: p.createVector(x, y),
                basePos: p.createVector(x, y),
                index: i
            });
        }

        // 创建粒子
        for (let i = 0; i < this.config.particleCount; i++) {
            this.particles.push(new DividerParticle(p, this));
        }

        p.background(10, 10, 15);
        this.timeOffset = 0;
    }

    draw(p) {
        // 半透明背景 (创建拖尾效果)
        p.background(10, 10, 15, this.config.backgroundAlpha);
        this.timeOffset += 0.01 * this.config.flowSpeed;

        // 动画化吸引点 (正弦波运动)
        for (let i = 0; i < this.attractors.length; i++) {
            const phase = i * p.PI / 4;
            const offset = p.sin(this.timeOffset * this.config.waveFrequency + phase) * this.config.waveAmplitude;
            this.attractors[i].pos.y = this.attractors[i].basePos.y + offset;
        }

        // 绘制吸引点 (可选)
        if (this.config.showAttractors) {
            for (let attractor of this.attractors) {
                p.noStroke();
                p.fill(this.config.accentColor + '60');
                p.ellipse(attractor.pos.x, attractor.pos.y, 12, 12);
                p.fill(this.config.accentColor);
                p.ellipse(attractor.pos.x, attractor.pos.y, 4, 4);
            }
        }

        // 更新和绘制粒子
        for (let particle of this.particles) {
            particle.update(p);
            particle.display(p);
        }
    }

    destroy() {
        if (this.p5Instance) {
            this.p5Instance.remove();
        }
    }
}

class DividerParticle {
    constructor(p, divider) {
        this.divider = divider;
        this.pos = p.createVector(p.random(divider.config.width), p.random(divider.config.height));
        this.vel = p.createVector(0, 0);
        this.acc = p.createVector(0, 0);
        this.trail = [];
        this.targetAttractor = p.floor(p.random(divider.attractors.length));
    }

    update(p) {
        const config = this.divider.config;
        const attractors = this.divider.attractors;

        // 强力吸引到目标吸引点
        let target = attractors[this.targetAttractor].pos;
        let force = p5.Vector.sub(target, this.pos);
        let distance = force.mag();

        if (distance < 20) {
            // 接近时切换到下一个吸引点
            this.targetAttractor = (this.targetAttractor + 1) % attractors.length;
        } else {
            distance = p.constrain(distance, 30, 300);
            let strength = 0.002 / (distance * distance);
            force.setMag(strength * config.flowSpeed);
            this.applyForce(force);
        }

        // 水平流动偏移 (从左到右)
        this.applyForce(p.createVector(0.01 * config.flowSpeed, 0));

        // 垂直居中力
        if (this.pos.y < config.height * 0.3 || this.pos.y > config.height * 0.7) {
            let centerForce = p.createVector(0, config.height/2 - this.pos.y);
            centerForce.mult(0.001);
            this.applyForce(centerForce);
        }

        // 水平环绕
        if (this.pos.x > config.width) {
            this.pos.x = 0;
            this.trail = [];
        }
        if (this.pos.x < 0) {
            this.pos.x = config.width;
            this.trail = [];
        }

        // 垂直约束
        this.pos.y = p.constrain(this.pos.y, 10, config.height - 10);

        this.vel.add(this.acc);
        this.vel.mult(0.96);
        this.vel.limit(6);
        this.pos.add(this.vel);
        this.acc.mult(0);

        this.trail.push(this.pos.copy());
        if (this.trail.length > config.trailLength) {
            this.trail.shift();
        }
    }

    applyForce(force) {
        this.acc.add(force);
    }

    display(p) {
        const config = this.divider.config;

        // 绘制拖尾
        for (let i = 1; i < this.trail.length; i++) {
            const alpha = p.map(i, 0, this.trail.length, 50, 255);
            const hexAlpha = Math.floor(alpha).toString(16).padStart(2, '0');
            p.stroke(config.accentColor + hexAlpha);
            p.strokeWeight(1.5);
            p.line(
                this.trail[i - 1].x,
                this.trail[i - 1].y,
                this.trail[i].x,
                this.trail[i].y
            );
        }

        // 绘制粒子
        p.noStroke();
        p.fill(config.accentColor);
        p.ellipse(this.pos.x, this.pos.y, 3, 3);
    }
}

// 导出到全局
if (typeof window !== 'undefined') {
    window.EmbeddedDivider = EmbeddedDivider;
}
