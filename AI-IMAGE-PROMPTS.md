# AI Image Generation Prompts for Physical AI Textbook

This file contains AI image generation prompts you can use with DALL-E, Midjourney, Stable Diffusion, or other AI image generators to create visuals for the textbook.

## Front Page Banner Image

**File name**: `static/img/physical-ai-banner.jpg`

**Recommended dimensions**: 1200x400px (3:1 ratio for banner)

**Prompt for AI Image Generator**:

```
A futuristic humanoid robot with sleek metallic design learning to interact with physical objects in a modern laboratory environment. The robot has expressive LED eyes showing curiosity and is reaching toward a colorful object on a table. Background shows advanced sensors, cameras, and motion tracking equipment. The scene conveys the intersection of artificial intelligence and physical embodiment. Photorealistic, cinematic lighting, educational illustration style, blue and white color scheme with orange accents. High detail, 8K quality.
```

**Alternative Prompt** (more abstract/conceptual):

```
Abstract visualization of Physical AI: A humanoid robot silhouette made of flowing data streams and neural networks, transitioning from digital (left side with binary code and circuits) to physical (right side with mechanical joints and sensors). The robot is reaching toward a glowing sphere representing the physical world. Background gradient from deep blue (digital) to warm orange (physical). Modern, minimalist, educational illustration. Vector art style, clean lines, professional.
```

**Alternative Prompt** (collaborative theme):

```
A humanoid robot and a human scientist working together at a collaborative workstation, examining a holographic display of robotic kinematics equations. The robot has a friendly, approachable design with blue LED indicators. The human is gesturing toward the display explaining something. Laboratory background with robotics equipment. The scene emphasizes human-robot collaboration in education and research. Bright, inviting colors, photorealistic style, educational setting. 16:9 aspect ratio.
```

---

## Chapter-Specific Images

### Chapter 1: Introduction to Physical AI

**File**: `docs/ch01-introduction/assets/embodied-intelligence.jpg`

**Prompt**:
```
An illustration showing the concept of embodied intelligence: A humanoid robot with transparent body revealing sensors (cameras in eyes, IMU in torso, force sensors in hands) and processing units (neural network visualization in head). The robot is surrounded by icons representing sensorimotor loop: perception (eye icon), decision (brain icon), action (hand icon), and feedback (circular arrows). Clean educational diagram style, labeled components, blue and white color scheme.
```

### Chapter 2: Robot Fundamentals

**File**: `docs/ch02-robot-fundamentals/assets/sensors-actuators.jpg`

**Prompt**:
```
Technical diagram showing various robot sensors and actuators arranged in a circular layout: IMU sensor, camera, LIDAR, force/torque sensor, electric motor, hydraulic actuator, and gripper. Each component is illustrated in isometric 3D style with labels and brief technical specifications. Central humanoid robot silhouette connecting all components. Professional engineering diagram aesthetic, blue gradient background, high clarity.
```

### Chapter 3: Humanoid Kinematics

**File**: `docs/ch03-kinematics/assets/forward-kinematics.jpg`

**Prompt**:
```
Educational illustration of robot kinematics: A robotic arm shown in three progressive states demonstrating forward kinematics. Left side shows joint angles (theta symbols with arrows), middle shows DH parameter frames (coordinate axes), right shows end-effector position reaching a target sphere. Mathematical equations float around showing transformation matrices. Clean technical illustration style, engineering diagram aesthetic, blue and orange color scheme.
```

### Chapter 4: Dynamics and Control

**File**: `docs/ch04-dynamics/assets/control-system.jpg`

**Prompt**:
```
Block diagram visualization of a robot control system: Central humanoid robot figure with overlaid control loop showing desired trajectory (dashed line), actual trajectory (solid line), PID controller block, dynamics model, and feedback sensors. Arrows show information flow. Mathematical symbols for position (q), velocity (q-dot), and torque (tau) labeled. Professional control systems diagram style, clear typography, educational illustration.
```

---

## How to Generate and Add Images

### Option 1: Using DALL-E (OpenAI)

1. Go to https://openai.com/dall-e-3
2. Sign in with your OpenAI account
3. Paste one of the prompts above
4. Generate the image
5. Download and save to the specified path
6. Rename to match the filename above

### Option 2: Using Midjourney

1. Join Midjourney Discord
2. Use command: `/imagine prompt: [paste prompt here]`
3. Select the best variation
4. Upscale and download
5. Save to the specified path

### Option 3: Using Stable Diffusion (Free)

1. Use https://stablediffusionweb.com/ or install locally
2. Paste the prompt
3. Adjust settings: Steps=50, CFG Scale=7, Size=1024x1024
4. Generate and download
5. Resize if needed and save to path

### Option 4: Using Microsoft Designer (Free)

1. Go to https://designer.microsoft.com/
2. Paste the prompt in the text box
3. Generate variations
4. Download your favorite
5. Save to the specified path

---

## Image Specifications

### Required Locations

1. **Front page banner**: `static/img/physical-ai-banner.jpg`
2. **Chapter assets**: `docs/ch0X-[chapter-name]/assets/[image-name].jpg`

### Size Guidelines

- Banner images: 1200x400px (3:1 ratio)
- Chapter header images: 800x400px (2:1 ratio)
- Diagram images: 800x600px (4:3 ratio)
- Icon images: 256x256px (1:1 ratio)

### Format

- Use **JPG** for photographs/realistic images (smaller file size)
- Use **PNG** for diagrams with transparency
- Use **SVG** for vector graphics when possible

### Optimization

After generating, optimize images for web:
```bash
# Using ImageMagick (install first)
convert input.jpg -quality 85 -resize 1200x400 output.jpg

# Using online tool
# Upload to tinypng.com or squoosh.app
```

---

## Current Status

- [ ] Front page banner (`/img/physical-ai-banner.jpg`)
- [ ] Chapter 1 assets
- [ ] Chapter 2 assets
- [ ] Chapter 3 assets
- [ ] Chapter 4 assets

**Next Steps**: Generate the front page banner first, then proceed with chapter-specific images as needed.

---

## Alternative: Use Free Stock Images

If you prefer not to generate AI images, you can use free stock images from:

- **Unsplash**: https://unsplash.com/s/photos/humanoid-robot
- **Pexels**: https://www.pexels.com/search/robotics/
- **Pixabay**: https://pixabay.com/images/search/robot/

Make sure to check licenses and provide attribution if required.
