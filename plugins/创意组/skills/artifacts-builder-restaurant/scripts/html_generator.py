#!/usr/bin/env python3
"""
HTML Artifact Generator for Restaurant Digital Presence
========================================================
Generates complete React component code for interactive H5 pages,
digital menus, promotional campaigns, and customer-facing interfaces.

Core Capabilities:
- H5 promotional page generation (grand opening, offers, events)
- Digital menu interface generation (with category tabs, search, filters)
- Reservation form generation
- Contact page generation
- Brand experience page generation
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Literal


# ============================================
# Configuration
# ============================================

@dataclass
class ArtifactConfig:
    """Artifact generation configuration"""
    artifact_type: Literal["h5-promo", "digital-menu", "reservation-form", "contact-page", "brand-story"]
    restaurant_name: str
    primary_color: str = "#DC143C"  # Red
    secondary_color: str = "#FFD700"  # Gold
    cuisine_type: str = "chinese"
    content: Dict = None


# ============================================
# Template Library
# ============================================

class ArtifactTemplates:
    """Library of React component templates"""

    @staticmethod
    def generate_h5_promo(config: ArtifactConfig) -> str:
        """Generate H5 promotional page (Grand Opening / Limited Offer)"""

        content = config.content or {}
        headline = content.get("headline", f"{config.restaurant_name}盛大开业")
        subheadline = content.get("subheadline", "全场钜惠,欢迎光临")
        opening_date = content.get("opening_date", "2025-02-15T10:00:00")
        offers = content.get("offers", [
            {"title": "第1重礼", "description": "前100名顾客免费赠送锅底"},
            {"title": "第2重礼", "description": "全场菜品8.8折优惠"},
            {"title": "第3重礼", "description": "充值500送100代金券"}
        ])
        address = content.get("address", "上海市徐汇区淮海中路XXX号")

        return f"""import React, {{ useState, useEffect }} from 'react';
import {{ Card, CardContent, CardHeader, CardTitle }} from '@/components/ui/card';
import {{ Button }} from '@/components/ui/button';
import {{ MapPin, Clock, Gift, Share2, Phone }} from 'lucide-react';

function {config.restaurant_name.replace(' ', '')}PromoPage() {{
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  function calculateTimeLeft() {{
    const openingDate = new Date('{opening_date}');
    const now = new Date();
    const difference = openingDate - now;

    if (difference <= 0) {{
      return {{ days: 0, hours: 0, minutes: 0, seconds: 0 }};
    }}

    return {{
      days: Math.floor(difference / (1000 * 60 * 60 * 24)),
      hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
      minutes: Math.floor((difference / 1000 / 60) % 60),
      seconds: Math.floor((difference / 1000) % 60)
    }};
  }}

  useEffect(() => {{
    const timer = setInterval(() => {{
      setTimeLeft(calculateTimeLeft());
    }}, 1000);
    return () => clearInterval(timer);
  }}, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-50 to-white">
      {{/* Hero Section */}}
      <section className="relative h-screen flex items-center justify-center bg-cover bg-center"
               style={{{{backgroundImage: 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1600)'}}}}>
        <div className="relative z-10 text-center text-white px-4 max-w-4xl">
          <h1 className="text-5xl md:text-7xl font-bold mb-4 animate-fade-in">
            {headline}
          </h1>
          <p className="text-2xl md:text-3xl mb-8">{subheadline}</p>
          <Button size="lg" className="bg-red-600 hover:bg-red-700 text-lg px-8 py-6">
            <Gift className="mr-2" /> 查看开业优惠
          </Button>
        </div>
      </section>

      {{/* Countdown Timer */}}
      <section className="py-16 px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-8">距离开业还有</h2>
        <div className="flex justify-center gap-4 flex-wrap">
          <CountdownCard value={{timeLeft.days}} label="天" />
          <CountdownCard value={{timeLeft.hours}} label="时" />
          <CountdownCard value={{timeLeft.minutes}} label="分" />
          <CountdownCard value={{timeLeft.seconds}} label="秒" />
        </div>
      </section>

      {{/* Opening Offers */}}
      <section className="py-16 px-4 bg-gradient-to-b from-red-50 to-white">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">开业钜惠</h2>
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
{self._generate_offer_cards(offers)}
        </div>
      </section>

      {{/* Location & Contact */}}
      <section className="py-16 px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">欢迎光临</h2>
        <div className="max-w-4xl mx-auto space-y-6">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-xl">
                <MapPin className="mr-2 text-red-600" /> 餐厅地址
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg mb-4">{address}</p>
              <Button variant="outline" className="w-full" size="lg">
                查看地图导航
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-xl">
                <Phone className="mr-2 text-red-600" /> 预订电话
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg mb-4">400-XXX-XXXX</p>
              <Button variant="outline" className="w-full" size="lg">
                立即拨打
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {{/* Social Share */}}
      <section className="py-16 px-4 text-center bg-red-50">
        <h2 className="text-2xl md:text-3xl font-bold mb-4">分享给好友</h2>
        <p className="text-gray-600 mb-6">分享开业喜讯,一起享受美食盛宴</p>
        <Button variant="outline" size="lg" className="border-red-600 text-red-600 hover:bg-red-50">
          <Share2 className="mr-2" /> 分享到微信
        </Button>
      </section>

      {{/* Footer */}}
      <footer className="py-8 px-4 text-center text-gray-600 border-t">
        <p>© 2025 {config.restaurant_name}. All rights reserved.</p>
      </footer>
    </div>
  );
}}

function CountdownCard({{ value, label }}) {{
  return (
    <Card className="w-24 md:w-32 hover:shadow-lg transition-shadow">
      <CardContent className="p-4 md:p-6 text-center">
        <div className="text-4xl md:text-5xl font-bold text-red-600">{{value}}</div>
        <div className="text-sm md:text-base text-gray-600 mt-2">{{label}}</div>
      </CardContent>
    </Card>
  );
}}

function OfferCard({{ icon, title, description }}) {{
  return (
    <Card className="hover:shadow-xl transition-all hover:-translate-y-1">
      <CardContent className="p-6 text-center">
        <div className="text-red-600 mb-4 flex justify-center">
          {{React.cloneElement(icon, {{ size: 56 }})}}
        </div>
        <h3 className="text-xl md:text-2xl font-bold mb-3">{{title}}</h3>
        <p className="text-gray-600 text-lg">{{description}}</p>
      </CardContent>
    </Card>
  );
}}

export default {config.restaurant_name.replace(' ', '')}PromoPage;
"""

    @staticmethod
    def _generate_offer_cards(offers: List[Dict]) -> str:
        """Helper to generate offer card components"""
        cards = []
        for offer in offers:
            cards.append(f"""          <OfferCard
            icon={{<Gift />}}
            title="{offer['title']}"
            description="{offer['description']}"
          />""")
        return "\n".join(cards)

    @staticmethod
    def generate_digital_menu(config: ArtifactConfig) -> str:
        """Generate digital menu interface with category tabs"""

        content = config.content or {}
        categories = content.get("categories", ["appetizers", "mains", "desserts", "drinks"])
        menu_data = content.get("menu_data", {
            "appetizers": [
                {"id": 1, "name": "夫妻肺片", "price": 38, "description": "经典川味凉菜,麻辣鲜香", "spicy": 3, "vegetarian": False},
                {"id": 2, "name": "口水鸡", "price": 42, "description": "嫩滑多汁,香辣可口", "spicy": 3, "vegetarian": False}
            ],
            "mains": [
                {"id": 10, "name": "毛血旺", "price": 78, "description": "重庆火锅经典菜品,麻辣重口", "spicy": 4, "vegetarian": False},
                {"id": 11, "name": "水煮鱼", "price": 88, "description": "鲜嫩鱼片配麻辣汤底", "spicy": 4, "vegetarian": False}
            ],
            "desserts": [
                {"id": 20, "name": "红糖糍粑", "price": 18, "description": "糯米糍粑配红糖浆", "spicy": 0, "vegetarian": True}
            ],
            "drinks": [
                {"id": 30, "name": "酸梅汤", "price": 12, "description": "传统解暑饮品", "spicy": 0, "vegetarian": True}
            ]
        })

        menu_data_json = json.dumps(menu_data, ensure_ascii=False, indent=4)

        return f"""import React, {{ useState }} from 'react';
import {{ Card, CardContent }} from '@/components/ui/card';
import {{ Input }} from '@/components/ui/input';
import {{ Badge }} from '@/components/ui/badge';
import {{ Tabs, TabsContent, TabsList, TabsTrigger }} from '@/components/ui/tabs';
import {{ Dialog, DialogContent, DialogHeader, DialogTitle }} from '@/components/ui/dialog';
import {{ Search, Flame, Leaf, Award }} from 'lucide-react';

function {config.restaurant_name.replace(' ', '')}DigitalMenu() {{
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDish, setSelectedDish] = useState(null);

  const menuData = {menu_data_json};

  const categoryNames = {{
    appetizers: '凉菜',
    mains: '热菜',
    desserts: '甜品',
    drinks: '饮品'
  }};

  const filteredMenu = Object.fromEntries(
    Object.entries(menuData).map(([category, dishes]) => [
      category,
      dishes.filter(dish =>
        dish.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        dish.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
    ])
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {{/* Header */}}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold text-center text-red-600">{config.restaurant_name}菜单</h1>
        </div>
      </header>

      {{/* Search Bar */}}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="relative">
          <Search className="absolute left-3 top-3 text-gray-400" />
          <Input
            type="text"
            placeholder="搜索菜品..."
            value={{searchTerm}}
            onChange={{(e) => setSearchTerm(e.target.value)}}
            className="pl-10 py-6 text-lg"
          />
        </div>
      </div>

      {{/* Menu Tabs */}}
      <div className="max-w-7xl mx-auto px-4 pb-8">
        <Tabs defaultValue="appetizers" className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            {{Object.keys(menuData).map(category => (
              <TabsTrigger key={{category}} value={{category}} className="text-base">
                {{categoryNames[category]}}
              </TabsTrigger>
            ))}}
          </TabsList>

          {{Object.entries(filteredMenu).map(([category, dishes]) => (
            <TabsContent key={{category}} value={{category}}>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {{dishes.map(dish => (
                  <DishCard
                    key={{dish.id}}
                    dish={{dish}}
                    onClick={{() => setSelectedDish(dish)}}
                  />
                ))}}
              </div>
              {{dishes.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  <p className="text-lg">未找到相关菜品</p>
                </div>
              )}}
            </TabsContent>
          ))}}
        </Tabs>
      </div>

      {{/* Dish Detail Modal */}}
      <Dialog open={{!!selectedDish}} onOpenChange={{() => setSelectedDish(null)}}>
        <DialogContent className="max-w-2xl">
          {{selectedDish && (
            <>
              <DialogHeader>
                <DialogTitle className="text-2xl">{{selectedDish.name}}</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden">
                  <img
                    src={{`https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80`}}
                    alt={{selectedDish.name}}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex items-center gap-2">
                  {{selectedDish.spicy > 0 && (
                    <Badge variant="destructive" className="flex items-center gap-1">
                      <Flame size={{14}} />
                      辣度: {{'🌶️'.repeat(selectedDish.spicy)}}
                    </Badge>
                  )}}
                  {{selectedDish.vegetarian && (
                    <Badge variant="outline" className="flex items-center gap-1">
                      <Leaf size={{14}} />
                      素食
                    </Badge>
                  )}}
                </div>
                <p className="text-gray-700 text-lg">{{selectedDish.description}}</p>
                <div className="flex items-center justify-between pt-4 border-t">
                  <span className="text-3xl font-bold text-red-600">
                    ¥{{selectedDish.price}}
                  </span>
                  <button className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-colors">
                    加入购物车
                  </button>
                </div>
              </div>
            </>
          )}}
        </DialogContent>
      </Dialog>
    </div>
  );
}}

function DishCard({{ dish, onClick }}) {{
  return (
    <Card
      className="hover:shadow-xl transition-all cursor-pointer hover:-translate-y-1"
      onClick={{onClick}}
    >
      <CardContent className="p-0">
        <div className="aspect-video bg-gray-200 overflow-hidden">
          <img
            src={{`https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&q=80`}}
            alt={{dish.name}}
            className="w-full h-full object-cover"
          />
        </div>
        <div className="p-4">
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-xl font-bold">{{dish.name}}</h3>
            <span className="text-lg font-bold text-red-600">¥{{dish.price}}</span>
          </div>
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">{{dish.description}}</p>
          <div className="flex items-center gap-2">
            {{dish.spicy > 0 && (
              <Badge variant="destructive" className="text-xs">
                <Flame size={{12}} className="mr-1" />
                {{'🌶️'.repeat(dish.spicy)}}
              </Badge>
            )}}
            {{dish.vegetarian && (
              <Badge variant="outline" className="text-xs">
                <Leaf size={{12}} className="mr-1" />
                素食
              </Badge>
            )}}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}}

export default {config.restaurant_name.replace(' ', '')}DigitalMenu;
"""

    @staticmethod
    def generate_reservation_form(config: ArtifactConfig) -> str:
        """Generate reservation form interface"""

        return f"""import React, {{ useState }} from 'react';
import {{ Card, CardContent, CardHeader, CardTitle }} from '@/components/ui/card';
import {{ Button }} from '@/components/ui/button';
import {{ Input }} from '@/components/ui/input';
import {{ Label }} from '@/components/ui/label';
import {{ Select, SelectContent, SelectItem, SelectTrigger, SelectValue }} from '@/components/ui/select';
import {{ Calendar }} from '@/components/ui/calendar';
import {{ Popover, PopoverContent, PopoverTrigger }} from '@/components/ui/popover';
import {{ Calendar as CalendarIcon, Clock, Users, CheckCircle }} from 'lucide-react';

function {config.restaurant_name.replace(' ', '')}ReservationForm() {{
  const [formData, setFormData] = useState({{
    name: '',
    phone: '',
    date: null,
    time: '',
    guests: '',
    notes: ''
  }});
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {{
    e.preventDefault();
    // In production, send data to backend
    console.log('Reservation submitted:', formData);
    setSubmitted(true);
  }};

  if (submitted) {{
    return (
      <div className="min-h-screen bg-gradient-to-b from-red-50 to-white flex items-center justify-center px-4">
        <Card className="max-w-md w-full text-center">
          <CardContent className="p-12">
            <CheckCircle className="w-20 h-20 text-green-500 mx-auto mb-4" />
            <h2 className="text-3xl font-bold mb-4">预订成功!</h2>
            <p className="text-gray-600 text-lg mb-6">
              我们已收到您的预订申请。稍后会有工作人员与您联系确认。
            </p>
            <Button
              onClick={{() => setSubmitted(false)}}
              className="w-full"
              size="lg"
            >
              返回
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }}

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-50 to-white py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">{config.restaurant_name}</h1>
          <p className="text-gray-600 text-lg">在线订座</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">预订信息</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={{handleSubmit}} className="space-y-6">
              {{/* Name */}}
              <div className="space-y-2">
                <Label htmlFor="name" className="text-base">姓名 *</Label>
                <Input
                  id="name"
                  type="text"
                  required
                  value={{formData.name}}
                  onChange={{(e) => setFormData({{...formData, name: e.target.value}})}}
                  placeholder="请输入您的姓名"
                  className="text-base py-6"
                />
              </div>

              {{/* Phone */}}
              <div className="space-y-2">
                <Label htmlFor="phone" className="text-base">手机号 *</Label>
                <Input
                  id="phone"
                  type="tel"
                  required
                  value={{formData.phone}}
                  onChange={{(e) => setFormData({{...formData, phone: e.target.value}})}}
                  placeholder="请输入您的手机号"
                  className="text-base py-6"
                />
              </div>

              {{/* Date */}}
              <div className="space-y-2">
                <Label className="text-base">就餐日期 *</Label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className="w-full justify-start text-left font-normal py-6 text-base"
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {{formData.date ? formData.date.toLocaleDateString('zh-CN') : '选择日期'}}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={{formData.date}}
                      onSelect={{(date) => setFormData({{...formData, date}})}}
                      disabled={{(date) => date < new Date()}}
                    />
                  </PopoverContent>
                </Popover>
              </div>

              {{/* Time */}}
              <div className="space-y-2">
                <Label htmlFor="time" className="text-base">就餐时间 *</Label>
                <Select
                  value={{formData.time}}
                  onValueChange={{(value) => setFormData({{...formData, time: value}})}}
                  required
                >
                  <SelectTrigger className="py-6 text-base">
                    <SelectValue placeholder="选择时间" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="11:00">11:00</SelectItem>
                    <SelectItem value="11:30">11:30</SelectItem>
                    <SelectItem value="12:00">12:00</SelectItem>
                    <SelectItem value="12:30">12:30</SelectItem>
                    <SelectItem value="13:00">13:00</SelectItem>
                    <SelectItem value="17:00">17:00</SelectItem>
                    <SelectItem value="17:30">17:30</SelectItem>
                    <SelectItem value="18:00">18:00</SelectItem>
                    <SelectItem value="18:30">18:30</SelectItem>
                    <SelectItem value="19:00">19:00</SelectItem>
                    <SelectItem value="19:30">19:30</SelectItem>
                    <SelectItem value="20:00">20:00</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {{/* Guests */}}
              <div className="space-y-2">
                <Label htmlFor="guests" className="text-base">就餐人数 *</Label>
                <Select
                  value={{formData.guests}}
                  onValueChange={{(value) => setFormData({{...formData, guests: value}})}}
                  required
                >
                  <SelectTrigger className="py-6 text-base">
                    <SelectValue placeholder="选择人数" />
                  </SelectTrigger>
                  <SelectContent>
                    {{[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                      <SelectItem key={{num}} value={{num.toString()}}>
                        {{num}} 人
                      </SelectItem>
                    ))}}
                    <SelectItem value="10+">10人以上</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {{/* Notes */}}
              <div className="space-y-2">
                <Label htmlFor="notes" className="text-base">特殊要求 (选填)</Label>
                <textarea
                  id="notes"
                  value={{formData.notes}}
                  onChange={{(e) => setFormData({{...formData, notes: e.target.value}})}}
                  placeholder="如有特殊要求请在此说明(如靠窗座位、婴儿座椅等)"
                  className="w-full min-h-[100px] p-3 border rounded-md text-base"
                />
              </div>

              {{/* Submit */}}
              <Button
                type="submit"
                className="w-full bg-red-600 hover:bg-red-700 text-lg py-6"
                size="lg"
              >
                确认预订
              </Button>

              <p className="text-sm text-gray-500 text-center">
                提交后我们会尽快与您联系确认
              </p>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}}

export default {config.restaurant_name.replace(' ', '')}ReservationForm;
"""


# ============================================
# HTML Artifact Generator
# ============================================

class HTMLArtifactGenerator:
    """Generate complete React component artifacts"""

    def __init__(self):
        self.templates = ArtifactTemplates()

    def generate(
        self,
        config: ArtifactConfig,
        output_dir: Optional[Path] = None,
        project_name: str = "餐饮H5页面"
    ) -> Dict:
        """
        Generate HTML artifact

        Args:
            config: Artifact configuration
            output_dir: Output directory
            project_name: Project name

        Returns:
            Generation result
        """

        # Set output directory
        if output_dir is None:
            output_dir = Path("output") / project_name / "X4-平面设计师" / "html-artifacts" / config.artifact_type

        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate component code
        if config.artifact_type == "h5-promo":
            component_code = self.templates.generate_h5_promo(config)
        elif config.artifact_type == "digital-menu":
            component_code = self.templates.generate_digital_menu(config)
        elif config.artifact_type == "reservation-form":
            component_code = self.templates.generate_reservation_form(config)
        else:
            raise ValueError(f"Unsupported artifact type: {config.artifact_type}")

        # Save component file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        component_filename = f"{config.restaurant_name.replace(' ', '-')}_{config.artifact_type}_{timestamp}.jsx"
        component_path = output_dir / component_filename
        component_path.write_text(component_code, encoding="utf-8")

        # Build metadata
        metadata = {
            "artifact_type": config.artifact_type,
            "restaurant_name": config.restaurant_name,
            "cuisine_type": config.cuisine_type,
            "primary_color": config.primary_color,
            "secondary_color": config.secondary_color,
            "timestamp": datetime.now().isoformat(),
            "component_path": str(component_path),
            "content": config.content
        }

        # Save metadata
        metadata_filename = f"{config.restaurant_name.replace(' ', '-')}_{config.artifact_type}_{timestamp}_metadata.json"
        metadata_path = output_dir / metadata_filename
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

        # Generate usage instructions
        instructions = f"""# {config.restaurant_name} - {config.artifact_type} 使用说明

## 文件信息
- **组件文件**: {component_filename}
- **创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **类型**: {config.artifact_type}

## 如何使用

### 方法1: Claude.ai Artifacts (推荐)

1. 访问 https://claude.ai
2. 新建对话
3. 输入: "请帮我创建一个React组件"
4. 将 {component_filename} 的完整代码复制粘贴到Claude
5. Claude会自动渲染交互式预览
6. 可以进一步调整样式、内容、功能

### 方法2: 本地开发环境

1. 确保已安装Node.js和npm
2. 创建新的React项目:
   ```bash
   npx create-react-app {config.restaurant_name.replace(' ', '-')}-app
   cd {config.restaurant_name.replace(' ', '-')}-app
   ```

3. 安装依赖:
   ```bash
   npm install lucide-react
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add card button input select tabs dialog calendar popover
   ```

4. 复制组件文件到 `src/` 目录

5. 在 `src/App.js` 中导入并使用:
   ```jsx
   import {config.restaurant_name.replace(' ', '')}{config.artifact_type.replace('-', ' ').title().replace(' ', '')} from './{component_filename}';

   function App() {{
     return <{config.restaurant_name.replace(' ', '')}{config.artifact_type.replace('-', ' ').title().replace(' ', '')} />;
   }}

   export default App;
   ```

6. 启动开发服务器:
   ```bash
   npm start
   ```

7. 浏览器访问 http://localhost:3000

## 定制化修改

### 修改颜色
在组件代码中搜索 `bg-red-600`, `text-red-600` 等类名,替换为你的品牌色。

### 修改内容
直接编辑组件代码中的文本内容、图片URL、菜单数据等。

### 添加功能
- 集成真实API (替换console.log为API调用)
- 连接后端数据库
- 添加支付功能
- 集成地图API
- 添加微信分享功能

## 技术栈
- **React**: UI框架
- **Tailwind CSS**: 样式框架
- **shadcn/ui**: UI组件库
- **Lucide React**: 图标库

## 浏览器兼容性
- Chrome 90+
- Safari 14+
- Firefox 88+
- Edge 90+

## 移动端优化
- 响应式布局
- 触摸友好的UI
- 44px最小触摸目标
- 快速加载
"""

        instructions_filename = f"{config.restaurant_name.replace(' ', '-')}_{config.artifact_type}_{timestamp}_使用说明.md"
        instructions_path = output_dir / instructions_filename
        instructions_path.write_text(instructions, encoding="utf-8")

        print(f"✅ HTML Artifact generated: {component_path}")
        print(f"📋 Metadata saved: {metadata_path}")
        print(f"📖 Instructions: {instructions_path}")
        print(f"\n{'='*60}")
        print("📢 NEXT STEPS:")
        print("="*60)
        print(f"\nReact component generated for {config.artifact_type}.")
        print(f"\nTo use this component:")
        print(f"1. Copy code from: {component_filename}")
        print(f"2. Open https://claude.ai and paste the code")
        print(f"3. Claude will render an interactive preview")
        print(f"4. Customize as needed and deploy")
        print(f"\nAlternatively, use in local React project (see usage instructions)")
        print(f"\n{'='*60}\n")

        return {
            "success": True,
            "component_path": str(component_path),
            "metadata_path": str(metadata_path),
            "instructions_path": str(instructions_path),
            "output_dir": str(output_dir),
            "metadata": metadata,
            "message": "HTML artifact generated successfully"
        }


# ============================================
# High-Level API
# ============================================

def generate_h5_promo(
    restaurant_name: str,
    headline: str,
    opening_date: str,
    offers: List[Dict],
    address: str,
    primary_color: str = "#DC143C",
    project_name: str = "H5开业促销页"
) -> Dict:
    """Generate H5 promotional page"""

    config = ArtifactConfig(
        artifact_type="h5-promo",
        restaurant_name=restaurant_name,
        primary_color=primary_color,
        content={
            "headline": headline,
            "opening_date": opening_date,
            "offers": offers,
            "address": address
        }
    )

    generator = HTMLArtifactGenerator()
    return generator.generate(config, project_name=project_name)


def generate_digital_menu(
    restaurant_name: str,
    menu_data: Dict,
    primary_color: str = "#DC143C",
    project_name: str = "数字菜单"
) -> Dict:
    """Generate digital menu interface"""

    config = ArtifactConfig(
        artifact_type="digital-menu",
        restaurant_name=restaurant_name,
        primary_color=primary_color,
        content={"menu_data": menu_data}
    )

    generator = HTMLArtifactGenerator()
    return generator.generate(config, project_name=project_name)


def generate_reservation_form(
    restaurant_name: str,
    primary_color: str = "#DC143C",
    project_name: str = "在线订座"
) -> Dict:
    """Generate reservation form"""

    config = ArtifactConfig(
        artifact_type="reservation-form",
        restaurant_name=restaurant_name,
        primary_color=primary_color
    )

    generator = HTMLArtifactGenerator()
    return generator.generate(config, project_name=project_name)


# ============================================
# CLI Interface
# ============================================

def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description="HTML Artifact Generator")
    parser.add_argument("type", choices=["h5-promo", "digital-menu", "reservation-form"],
                       help="Artifact type")
    parser.add_argument("restaurant_name", help="Restaurant name")
    parser.add_argument("--project", default="餐饮H5页面", help="Project name")

    args = parser.parse_args()

    if args.type == "h5-promo":
        result = generate_h5_promo(
            restaurant_name=args.restaurant_name,
            headline=f"{args.restaurant_name}盛大开业",
            opening_date="2025-02-15T10:00:00",
            offers=[
                {"title": "第1重礼", "description": "前100名顾客免费赠送锅底"},
                {"title": "第2重礼", "description": "全场菜品8.8折优惠"},
                {"title": "第3重礼", "description": "充值500送100代金券"}
            ],
            address="上海市徐汇区淮海中路XXX号",
            project_name=args.project
        )
    elif args.type == "digital-menu":
        result = generate_digital_menu(
            restaurant_name=args.restaurant_name,
            menu_data={},  # Use default demo data
            project_name=args.project
        )
    elif args.type == "reservation-form":
        result = generate_reservation_form(
            restaurant_name=args.restaurant_name,
            project_name=args.project
        )

    if result["success"]:
        print(f"\n✨ Artifact generated successfully!")
        print(f"📁 Component: {result['component_path']}")
        print(f"📋 Metadata: {result['metadata_path']}")
        print(f"📖 Instructions: {result['instructions_path']}")
    else:
        print(f"\n❌ Generation failed: {result.get('error')}")


if __name__ == "__main__":
    main()
