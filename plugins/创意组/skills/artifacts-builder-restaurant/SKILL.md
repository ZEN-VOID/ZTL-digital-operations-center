---
name: artifacts-builder-restaurant
description: Build complex, interactive HTML artifacts for restaurant digital presence using React, Tailwind CSS, and shadcn/ui. Create H5 promotional pages, digital menus, online ordering interfaces, reservation systems, and brand experience pages optimized for mobile devices.
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# Restaurant Artifacts Builder

Create sophisticated, interactive HTML artifacts for restaurant digital marketing and operations. Build mobile-optimized H5 pages, digital menus, promotional campaigns, and customer-facing web applications using modern web technologies (React, Tailwind CSS, shadcn/ui).

## Core Capabilities

### 1. Artifact Types for Restaurants

**H5 Promotional Pages**:
- Grand opening announcements
- Limited-time offers and promotions
- New menu launches
- Holiday/seasonal campaigns
- Event invitations
- Contest and giveaway pages

**Digital Menus**:
- Interactive menu browsing
- Dish detail pages with photos and descriptions
- Dietary filters (vegetarian, gluten-free, spicy level)
- Category navigation
- Search functionality
- Multi-language support

**Brand Experience Pages**:
- Restaurant story and philosophy
- Chef profiles and kitchen stories
- Behind-the-scenes content
- Virtual restaurant tours
- Sustainability initiatives
- Community involvement

**Operational Interfaces**:
- Table reservation forms
- Online ordering (delivery/pickup)
- Loyalty program enrollment
- Gift card purchases
- Catering inquiry forms
- Contact and feedback forms

### 2. Technical Stack

**Frontend Framework**: React (via claude.ai artifact builder)
**Styling**: Tailwind CSS (utility-first, responsive)
**Components**: shadcn/ui (accessible, customizable)
**Icons**: Lucide React
**Animations**: CSS transitions, Framer Motion (if needed)
**Mobile-First**: Optimized for mobile devices

### 3. Design Principles

**Mobile Optimization**:
- Touch-friendly UI (44px minimum tap targets)
- Thumb-zone prioritization
- Fast loading (lazy loading images)
- Smooth scrolling and transitions
- Responsive layouts (breakpoints: sm, md, lg, xl)

**User Experience**:
- Clear call-to-action buttons
- Intuitive navigation
- Minimal form fields
- Visual feedback for interactions
- Error handling and validation
- Loading states

**Performance**:
- Optimized images (WebP format, lazy loading)
- Code splitting
- Minimal dependencies
- CSS-only animations where possible
- Fast initial load (< 3 seconds)

**Accessibility**:
- ARIA labels and roles
- Keyboard navigation
- Screen reader support
- Sufficient color contrast (WCAG AA)
- Focus indicators

## Quick Start: Build H5 Promotional Page

### Example 1: Grand Opening Promotion

**Use Case**: Announce restaurant grand opening with special offers

**Features**:
- Hero section with restaurant photo and headline
- Countdown timer to opening day
- Opening offers section (discounts, free items)
- Location map and directions
- Social media follow buttons
- Share functionality

**Code Structure**:
```jsx
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MapPin, Clock, Gift, Share2 } from 'lucide-react';

function GrandOpeningPage() {
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  function calculateTimeLeft() {
    const openingDate = new Date('2025-02-15T10:00:00');
    const now = new Date();
    const difference = openingDate - now;

    return {
      days: Math.floor(difference / (1000 * 60 * 60 * 24)),
      hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
      minutes: Math.floor((difference / 1000 / 60) % 60),
      seconds: Math.floor((difference / 1000) % 60)
    };
  }

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-50 to-white">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center bg-cover bg-center"
               style={{backgroundImage: 'url(/hero-restaurant.jpg)'}}>
        <div className="absolute inset-0 bg-black/50"></div>
        <div className="relative z-10 text-center text-white px-4">
          <h1 className="text-5xl md:text-7xl font-bold mb-4">
            川香火锅
          </h1>
          <p className="text-2xl md:text-3xl mb-8">盛大开业</p>
          <Button size="lg" className="bg-red-600 hover:bg-red-700">
            <Gift className="mr-2" /> 查看开业优惠
          </Button>
        </div>
      </section>

      {/* Countdown Timer */}
      <section className="py-16 px-4">
        <h2 className="text-3xl font-bold text-center mb-8">距离开业还有</h2>
        <div className="flex justify-center gap-4 flex-wrap">
          <CountdownCard value={timeLeft.days} label="天" />
          <CountdownCard value={timeLeft.hours} label="时" />
          <CountdownCard value={timeLeft.minutes} label="分" />
          <CountdownCard value={timeLeft.seconds} label="秒" />
        </div>
      </section>

      {/* Opening Offers */}
      <section className="py-16 px-4 bg-red-50">
        <h2 className="text-3xl font-bold text-center mb-12">开业钜惠</h2>
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          <OfferCard
            icon={<Gift />}
            title="第1重礼"
            description="前100名顾客免费赠送锅底"
          />
          <OfferCard
            icon={<Gift />}
            title="第2重礼"
            description="全场菜品8.8折优惠"
          />
          <OfferCard
            icon={<Gift />}
            title="第3重礼"
            description="充值500送100代金券"
          />
        </div>
      </section>

      {/* Location & Contact */}
      <section className="py-16 px-4">
        <h2 className="text-3xl font-bold text-center mb-12">欢迎光临</h2>
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <MapPin className="mr-2" /> 餐厅地址
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4">上海市徐汇区淮海中路XXX号</p>
              <Button variant="outline" className="w-full">
                查看地图导航
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Social Share */}
      <section className="py-16 px-4 text-center">
        <h2 className="text-2xl font-bold mb-4">分享给好友</h2>
        <Button variant="outline" size="lg">
          <Share2 className="mr-2" /> 分享到微信
        </Button>
      </section>
    </div>
  );
}

function CountdownCard({ value, label }) {
  return (
    <Card className="w-24">
      <CardContent className="p-4 text-center">
        <div className="text-4xl font-bold text-red-600">{value}</div>
        <div className="text-sm text-gray-600">{label}</div>
      </CardContent>
    </Card>
  );
}

function OfferCard({ icon, title, description }) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardContent className="p-6 text-center">
        <div className="text-red-600 mb-4 flex justify-center">
          {React.cloneElement(icon, { size: 48 })}
        </div>
        <h3 className="text-xl font-bold mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </CardContent>
    </Card>
  );
}

export default GrandOpeningPage;
```

### Example 2: Digital Menu Interface

**Use Case**: Interactive menu browsing on mobile devices

**Features**:
- Category tabs (appetizers, mains, desserts, drinks)
- Dish cards with photo, name, description, price
- Dietary icons (vegetarian, spicy, gluten-free)
- Search bar
- Filter by dietary preferences
- Dish detail modal with full description

**Code Structure**:
```jsx
import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Search, Flame, Leaf } from 'lucide-react';

function DigitalMenu() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDish, setSelectedDish] = useState(null);

  const menuData = {
    appetizers: [
      {
        id: 1,
        name: '夫妻肺片',
        price: 38,
        description: '经典川味凉菜,麻辣鲜香',
        spicy: 3,
        vegetarian: false,
        image: '/dish-feipi.jpg'
      },
      // ... more dishes
    ],
    mains: [
      {
        id: 10,
        name: '毛血旺',
        price: 78,
        description: '重庆火锅经典菜品,麻辣重口',
        spicy: 4,
        vegetarian: false,
        image: '/dish-maoxuewang.jpg'
      },
      // ... more dishes
    ],
    // ... other categories
  };

  const filteredMenu = Object.fromEntries(
    Object.entries(menuData).map(([category, dishes]) => [
      category,
      dishes.filter(dish =>
        dish.name.includes(searchTerm) ||
        dish.description.includes(searchTerm)
      )
    ])
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-red-600 text-white p-4 sticky top-0 z-10">
        <h1 className="text-2xl font-bold text-center mb-4">川香火锅菜单</h1>
        <div className="relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <Input
            type="text"
            placeholder="搜索菜品..."
            className="pl-10 bg-white"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </header>

      {/* Menu Categories */}
      <Tabs defaultValue="appetizers" className="p-4">
        <TabsList className="grid grid-cols-4 w-full mb-6">
          <TabsTrigger value="appetizers">凉菜</TabsTrigger>
          <TabsTrigger value="mains">主菜</TabsTrigger>
          <TabsTrigger value="desserts">甜品</TabsTrigger>
          <TabsTrigger value="drinks">饮品</TabsTrigger>
        </TabsList>

        <TabsContent value="appetizers">
          <DishGrid dishes={filteredMenu.appetizers} onSelectDish={setSelectedDish} />
        </TabsContent>
        <TabsContent value="mains">
          <DishGrid dishes={filteredMenu.mains} onSelectDish={setSelectedDish} />
        </TabsContent>
        {/* ... other categories */}
      </Tabs>

      {/* Dish Detail Modal */}
      {selectedDish && (
        <DishDetailModal dish={selectedDish} onClose={() => setSelectedDish(null)} />
      )}
    </div>
  );
}

function DishGrid({ dishes, onSelectDish }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {dishes.map(dish => (
        <DishCard key={dish.id} dish={dish} onClick={() => onSelectDish(dish)} />
      ))}
    </div>
  );
}

function DishCard({ dish, onClick }) {
  return (
    <Card className="cursor-pointer hover:shadow-lg transition-shadow" onClick={onClick}>
      <CardContent className="p-0">
        <img
          src={dish.image}
          alt={dish.name}
          className="w-full h-48 object-cover rounded-t-lg"
        />
        <div className="p-4">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-bold">{dish.name}</h3>
            <span className="text-red-600 font-bold text-lg">¥{dish.price}</span>
          </div>
          <p className="text-gray-600 text-sm mb-2">{dish.description}</p>
          <div className="flex gap-2">
            {dish.spicy > 0 && (
              <Badge variant="destructive" className="flex items-center gap-1">
                <Flame size={14} /> {Array(dish.spicy).fill('🌶').join('')}
              </Badge>
            )}
            {dish.vegetarian && (
              <Badge variant="secondary" className="flex items-center gap-1">
                <Leaf size={14} /> 素食
              </Badge>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function DishDetailModal({ dish, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-end md:items-center justify-center"
         onClick={onClose}>
      <div className="bg-white rounded-t-2xl md:rounded-2xl w-full md:max-w-2xl max-h-[90vh] overflow-y-auto"
           onClick={(e) => e.stopPropagation()}>
        <img
          src={dish.image}
          alt={dish.name}
          className="w-full h-64 object-cover"
        />
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-2">{dish.name}</h2>
          <p className="text-3xl text-red-600 font-bold mb-4">¥{dish.price}</p>
          <p className="text-gray-700 mb-6">{dish.description}</p>

          <div className="flex gap-2 mb-6">
            {dish.spicy > 0 && (
              <Badge variant="destructive">
                辣度: {Array(dish.spicy).fill('🌶').join('')}
              </Badge>
            )}
            {dish.vegetarian && <Badge variant="secondary">素食</Badge>}
          </div>

          <Button className="w-full bg-red-600 hover:bg-red-700" onClick={onClose}>
            关闭
          </Button>
        </div>
      </div>
    </div>
  );
}

export default DigitalMenu;
```

## Artifact Templates Library

### Template 1: H5 Promotional Page

**Structure**:
- Hero section with background image
- Key message and CTA
- Features/benefits section
- Social proof (reviews, testimonials)
- Call-to-action footer
- Share functionality

**Styling Guidelines**:
- Mobile-first responsive design
- Large, touch-friendly buttons (min 44px height)
- Clear visual hierarchy
- Brand colors prominent
- Fast loading optimizations

### Template 2: Digital Menu

**Structure**:
- Sticky header with search
- Category tabs/navigation
- Dish cards (image, name, price, icons)
- Filter options
- Detail modal/page
- Back to top button

**Styling Guidelines**:
- High-quality food imagery
- Clear pricing
- Dietary icons visible
- Easy scrolling navigation
- Thumb-zone optimization

### Template 3: Reservation Form

**Structure**:
- Date and time picker
- Party size selector
- Contact information fields
- Special requests textarea
- Confirmation screen
- Cancellation policy

**Styling Guidelines**:
- Minimal form fields
- Clear labels and placeholders
- Real-time validation
- Progress indicators
- Success confirmation

### Template 4: Brand Story Page

**Structure**:
- Hero with brand video/image
- Timeline of restaurant history
- Chef profiles
- Values and philosophy
- Behind-the-scenes photos
- Community involvement

**Styling Guidelines**:
- Storytelling flow
- Rich media (images, videos)
- Emotional connection
- Brand personality shine
- Shareable content

## Tailwind CSS Utilities for Restaurants

### Color Utilities

**Chinese Restaurant**:
```css
bg-red-600      /* Primary brand color */
text-red-600    /* Text accent */
bg-amber-400    /* Gold accents */
hover:bg-red-700 /* Interactive states */
```

**Japanese Restaurant**:
```css
bg-slate-900    /* Dark elegant */
bg-white        /* Clean white */
text-amber-600  /* Accent gold */
bg-gray-50      /* Subtle background */
```

**Italian Restaurant**:
```css
bg-green-700    /* Basil green */
bg-red-600      /* Tomato red */
bg-amber-100    /* Warm neutral */
hover:bg-green-800
```

### Spacing & Layout

```css
p-4             /* Padding 1rem */
px-4 py-6       /* Horizontal & vertical padding */
gap-4           /* Grid/flex gap */
max-w-6xl       /* Container max width */
mx-auto         /* Center container */
```

### Typography

```css
text-3xl font-bold     /* Large headings */
text-lg font-medium    /* Subheadings */
text-sm text-gray-600  /* Body text */
leading-relaxed        /* Line height */
```

### Responsive Design

```css
/* Mobile first */
grid-cols-1              /* Single column on mobile */
md:grid-cols-2          /* 2 columns on medium screens */
lg:grid-cols-3          /* 3 columns on large screens */

text-2xl                /* Base size */
md:text-3xl             /* Larger on medium screens */
lg:text-4xl             /* Largest on large screens */
```

## shadcn/ui Components for Restaurants

### Essential Components

**Card**: Dish cards, offer cards, content sections
```jsx
<Card>
  <CardHeader><CardTitle>菜品名称</CardTitle></CardHeader>
  <CardContent>菜品详情</CardContent>
</Card>
```

**Button**: CTAs, actions, navigation
```jsx
<Button variant="default" size="lg">立即预订</Button>
<Button variant="outline">查看详情</Button>
```

**Input**: Search, forms, filters
```jsx
<Input type="text" placeholder="搜索菜品..." />
<Input type="tel" placeholder="手机号码" />
```

**Tabs**: Menu categories, content sections
```jsx
<Tabs defaultValue="mains">
  <TabsList>
    <TabsTrigger value="mains">主菜</TabsTrigger>
    <TabsTrigger value="desserts">甜品</TabsTrigger>
  </TabsList>
  <TabsContent value="mains">{/* Content */}</TabsContent>
</Tabs>
```

**Badge**: Dietary icons, labels, status
```jsx
<Badge variant="destructive">辣</Badge>
<Badge variant="secondary">素食</Badge>
```

**Dialog/Modal**: Dish details, confirmations
```jsx
<Dialog>
  <DialogTrigger>查看详情</DialogTrigger>
  <DialogContent>
    <DialogHeader><DialogTitle>菜品详情</DialogTitle></DialogHeader>
    {/* Dish details */}
  </DialogContent>
</Dialog>
```

## Mobile Optimization Checklist

✅ **Touch Targets**:
- [ ] Buttons minimum 44px × 44px
- [ ] Adequate spacing between tap targets (8px minimum)
- [ ] Bottom navigation in thumb zone

✅ **Performance**:
- [ ] Images optimized and lazy loaded
- [ ] Code split for faster initial load
- [ ] Minimal third-party scripts
- [ ] CSS animations over JavaScript

✅ **User Experience**:
- [ ] Smooth scrolling
- [ ] Pull-to-refresh (if applicable)
- [ ] Loading states for async actions
- [ ] Error messages clear and actionable
- [ ] Back button behavior intuitive

✅ **Responsive Layout**:
- [ ] Mobile-first approach
- [ ] Breakpoints: sm (640px), md (768px), lg (1024px)
- [ ] Typography scales appropriately
- [ ] Images scale without distortion

✅ **Accessibility**:
- [ ] ARIA labels on interactive elements
- [ ] Sufficient color contrast (4.5:1)
- [ ] Keyboard navigation support
- [ ] Screen reader friendly

## Output Path Convention

Artifacts save to:
```
output/[项目名]/X3-平面设计师/artifacts/
├── h5-pages/
│   ├── [campaign-name]-h5.html
│   └── [campaign-name]-preview.jpg
├── digital-menus/
│   ├── [restaurant-name]-menu.html
│   └── [restaurant-name]-menu-mobile.mp4 (demo)
├── forms/
│   ├── [form-type]-form.html
│   └── [form-type]-schema.json
└── brand-pages/
    ├── [page-name].html
    └── assets/
        ├── images/
        └── videos/
```

## Integration with Design Workflow

**For X3-平面设计师**:

1. **Planning Phase**:
   - Review artifact requirements (H5 page, menu, form, etc.)
   - Define user flows and interactions
   - Select appropriate template or build custom
   - Determine brand theme and styling

2. **Design Phase**:
   - Apply brand guidelines and theme
   - Create high-fidelity mockups (Figma/Sketch)
   - Define component hierarchy
   - Plan responsive breakpoints

3. **Build Phase**:
   - Start with template or blank artifact
   - Implement React components
   - Apply Tailwind styling
   - Integrate shadcn/ui components
   - Add interactivity and state management

4. **Testing Phase**:
   - Test on actual mobile devices
   - Verify touch interactions
   - Check performance (loading speed)
   - Validate accessibility
   - Cross-browser testing

5. **Delivery Phase**:
   - Export HTML artifact
   - Provide usage documentation
   - Include deployment instructions
   - Archive source code

## Best Practices

1. **Component Reusability**: Build modular, reusable components
2. **State Management**: Use React hooks (useState, useEffect) appropriately
3. **Performance**: Lazy load images, minimize re-renders
4. **Accessibility**: Always include ARIA labels and semantic HTML
5. **Mobile-First**: Design and build for mobile, then enhance for desktop
6. **Brand Consistency**: Apply brand guidelines and theme systematically
7. **User Testing**: Get feedback on real devices from actual users
8. **Documentation**: Comment complex logic, document component props

## Common Pitfalls to Avoid

❌ **Desktop-First Thinking**: Designing for desktop then adapting to mobile
❌ **Heavy Assets**: Using unoptimized large images
❌ **Complex Navigation**: Deep menu hierarchies on mobile
❌ **Tiny Touch Targets**: Buttons smaller than 44px
❌ **Auto-Playing Media**: Videos/audio that play without user action
❌ **Ignoring Loading States**: No feedback during async operations
❌ **Poor Contrast**: Text difficult to read on backgrounds
❌ **Horizontal Scrolling**: Content requiring horizontal scroll on mobile

---

**Remember**: Great artifacts balance aesthetics, functionality, and performance. They should look beautiful, work seamlessly, and load quickly. Always prioritize the user experience—especially on mobile devices where the majority of restaurant customers will interact with your work.
