# MiniMax Video Prompt Optimizer - Extended Reference

## Complete Camera Movement Guide

### All 15 Camera Movements with Examples

#### 1. Truck Left / Truck Right
**Motion**: Camera moves parallel to subject, sideways
**Use Case**: Follow action, reveal scene horizontally
**Example**: `[Truck right] Following waiter carrying hotpot through dining room`

#### 2. Pan Left / Pan Right
**Motion**: Camera rotates horizontally on fixed position
**Use Case**: Reveal environment, show spatial relationship
**Example**: `[Pan left] Restaurant entrance revealing full dining area`

#### 3. Push In / Pull Out
**Motion**: Camera physically moves toward/away from subject
**Use Case**: Focus attention, establish scene
**Example**: `[Push in] Close-up of bubbling hotpot, [Pull out] revealing full table`

#### 4. Pedestal Up / Pedestal Down
**Motion**: Camera moves vertically up/down
**Use Case**: Change perspective, reveal height
**Example**: `[Pedestal up] From table level to overhead shot of restaurant`

#### 5. Tilt Up / Tilt Down
**Motion**: Camera rotates vertically on fixed position
**Use Case**: Reveal vertical elements, dramatic reveal
**Example**: `[Tilt down] From restaurant sign to entrance door`

#### 6. Zoom In / Zoom Out
**Motion**: Lens optical zoom (no camera movement)
**Use Case**: Focus detail, dramatic emphasis
**Example**: `[Zoom in] Focusing on steam rising from hotpot`

#### 7. Shake
**Motion**: Handheld unstable camera movement
**Use Case**: Urgency, energy, documentary feel
**Example**: `[Shake] Dynamic stir-fry cooking action in wok`

#### 8. Tracking Shot
**Motion**: Camera follows moving subject smoothly
**Use Case**: Follow action, immersive following
**Example**: `[Tracking shot] Following chef preparing signature dish`

#### 9. Static Shot
**Motion**: No camera movement
**Use Case**: Stable composition, focus on subject motion
**Example**: `[Static shot] Steam rising from hotpot, elegant presentation`

## Model Comparison Matrix

| Feature | T2V-01 | T2V-01-Director | I2V-01 | I2V-01-Director | I2V-01-live | Hailuo-02 |
|---------|--------|-----------------|---------|-----------------|-------------|-----------|
| **Input** | Text only | Text only | Text + Image | Text + Image | Text + Image | Text (or Text + Image) |
| **Camera Control** | No | Yes (15 moves) | No | Yes (15 moves) | No | Yes (15 moves) |
| **Duration** | 6s | 6s | 6s | 6s | 6s | 6s or 10s |
| **Resolution** | Standard | Standard | Standard | Standard | Standard | 768P / 1080P |
| **Best For** | Quick gen | Cinematic | Animate photo | Cinematic photo | Live action | Premium quality |
| **Complexity** | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

## Restaurant Video Production Workflow

### Phase 1: Pre-Production
1. **Define Purpose**: Menu showcase, environment tour, promo, social media
2. **Gather Assets**: Dish photos (for I2V), reference videos, brand guidelines
3. **Script Key Shots**: List must-have visuals (e.g., signature dish, dining area)
4. **Select Model**: Match purpose to model (see decision tree in SKILL.md)

### Phase 2: Prompt Engineering
1. **Draft Base Prompt**: Subject + Motion + Aesthetic
2. **Add Camera Movements**: 1-2 movements for Director mode
3. **Optimize for API**: Validate format, length, syntax
4. **A/B Test Variations**: Try different camera angles

### Phase 3: Generation
1. **Call API**: Use optimized prompt
2. **Monitor Progress**: Check async status if needed
3. **Review Output**: Validate quality and relevance
4. **Iterate if Needed**: Adjust prompt based on results

### Phase 4: Post-Production
1. **Trim/Edit**: Combine multiple 6s clips for longer video
2. **Add Audio**: Overlay music from X10 (music optimizer)
3. **Add Text/Graphics**: Branding, captions, CTAs
4. **Export for Platform**: Instagram (768P), TikTok (1080P), Website (1080P)

## Edge Case Handling

### Very Short Briefs
**Input**: "火锅"
**Strategy**: Expand with restaurant-specific defaults
**Output**: `Close-up of bubbling Sichuan hotpot with fresh ingredients, steam rising, warm appetizing lighting`

### Conflicting Camera Movements
**Input**: `"左移然后右移"` (pan left then pan right)
**Strategy**: Choose primary direction based on context
**Resolution**: Use `[Pan left]` only, note conflict

### Invalid First Frame Path
**Input**: `first_frame_image="nonexistent.jpg"`
**Strategy**: Validate file existence, fallback to T2V if missing
**Fallback**: Switch to T2V-01-Director with similar composition

### Excessive Camera Movements
**Input**: 5+ camera movements requested
**Strategy**: Prioritize first 2, log truncation
**Result**: Keep `[Push in, Tilt down]`, drop rest

## API Error Handling

### Common Errors
- `INVALID_MODEL`: Model name typo → Auto-correct to valid model
- `MISSING_FIRST_FRAME`: I2V without image → Fallback to T2V
- `INVALID_DURATION`: Duration not 6 or 10 → Default to 6
- `CONCURRENT_LIMIT`: Another video generating → Wait or use async_mode

### Retry Strategy
```python
def call_with_retry(api_params, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = mcp__minimax-mcp__generate_video(**api_params)
            return result
        except Exception as e:
            if "CONCURRENT_LIMIT" in str(e) and attempt < max_retries - 1:
                time.sleep(10)  # Wait 10s before retry
                continue
            raise
```

## Performance Optimization

### Batch Generation Strategy
- Generate multiple videos sequentially (1 concurrent limit)
- Use async_mode for large batches
- Monitor with `query_video_generation` tool

### Prompt Caching
- Cache restaurant-specific templates
- Reuse successful prompt patterns
- Store optimization results for similar requests

## Troubleshooting

### Issue: "Video doesn't match prompt"
- **Check**: Camera movement syntax `[Movement]` not `{Movement}`
- **Check**: Model supports requested features (duration/resolution)
- **Fix**: Simplify prompt, reduce camera movements to 1-2

### Issue: "Video is shaky/unstable"
- **Cause**: Too many camera movements (3+)
- **Fix**: Reduce to 1-2 movements, avoid conflicting directions

### Issue: "Subject not in focus"
- **Cause**: Vague subject description
- **Fix**: Add specific details: "Close-up of", "featuring", "focusing on"

## Version History

- **v1.0.0** (2025-10-30): Initial release with all 5 models support

## License

**Author**: ZTL Digital Intelligence Operations Center - 创意组
**License**: MIT
