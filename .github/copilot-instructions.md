# AutomatedTrendHunting - AI Coding Agent Instructions

## 🎯 Project Overview

This is a trend hunting application that automatically identifies emerging trends by analyzing data from Google Trends and Reddit. The goal is to create a monetizable SaaS platform that helps users discover market opportunities early.

## 📋 Project Context & Planning

- **Current Status**: Early development phase (planning/checklist stage)
- **Primary Reference**: `Checklist.md` contains the complete development roadmap
- **Target Language**: Portuguese (PT-BR) - maintain this for user-facing content
- **Architecture Goal**: Simple, scalable web application with automated data collection

## 🛠️ Technical Architecture (Planned)

### Core Components

1. **Data Collection Engine**: Google Trends API + Reddit scraping/API integration
2. **Scoring System**: Custom algorithm to rank and detect emerging trends
3. **Data Storage**: Database with caching layer for performance
4. **Frontend**: Responsive web interface with trend visualization
5. **Automation**: Scheduled jobs for data updates and trend detection
6. **Monetization**: Freemium model with Google AdSense and premium features

### Key Integration Points

- **Google Trends API**: Primary data source for trend metrics
- **Reddit API/Scraping**: Secondary validation and community sentiment
- **Deployment**: Planned for Vercel/Netlify for easy scaling
- **Monitoring**: Basic analytics and performance tracking

## 💡 Development Workflows

### Priority Order (from Checklist.md)

1. **MVP Core**: Data collection system (Google Trends + Reddit)
2. **Basic Frontend**: Trend list with filtering and search
3. **Automation**: Background jobs for data updates
4. **Monetization**: AdSense integration and user system
5. **Marketing**: Analytics, landing page, beta launch

### Key Commands & Patterns

- Follow the checklist progression: Infrastructure → Core features → UI → Monetization
- Implement caching early to handle API rate limits
- Design for multiple data sources from the start
- Plan for premium features (email alerts, API access, advanced analytics)

## 🎨 UI/UX Conventions

### Planned Features

- **Responsive design**: Mobile-first approach
- **Dark/Light mode**: User preference toggle
- **Performance optimization**: Loading states, pagination
- **Filtering system**: By category, time range, growth metrics
- **Visualization**: Basic charts for trend data
- **Simple navigation**: Trend list → Detail pages → Search

## 📊 Data Patterns

### Trend Scoring Algorithm

- Combine growth rate, volume, and timeline data
- Weight different sources (Google Trends vs Reddit sentiment)
- Implement category-based filtering (3-5 target niches)
- Cache frequently accessed data to reduce API calls

### Database Design Considerations

- Store trend history for analysis
- User profiles for premium features
- Alert preferences and notification logs
- Category taxonomies for filtering

## 🚀 Development Guidelines

### File Organization

- Keep the checklist updated as features are completed
- Document API integrations thoroughly due to rate limits
- Create modular components for different data sources
- Plan for horizontal scaling from the beginning

### Testing Strategy

- Test API integrations with mock data first
- Validate trend scoring algorithm with historical data
- Beta test with small user group (target: 10 initial users)
- Monitor performance under data collection load

## 💰 Business Logic

### Monetization Approach

- **Free tier**: Basic trend viewing with ads (Google AdSense)
- **Premium tier**: Ad-free, email alerts, advanced filters
- **Developer API**: Paid access for third-party integrations
- **Affiliate partnerships**: Relevant tool recommendations

### Growth Strategy

- Launch in relevant communities (Reddit, HackerNews, IndieHackers)
- Weekly newsletter with trend insights
- Referral program for user acquisition
- Social media presence for trend announcements

## 🔧 Technical Debt & Considerations

### API Rate Limits

- Implement proper caching strategies early
- Plan for Google Trends API quotas
- Consider Reddit API alternatives if needed
- Design graceful degradation for API failures

### Scalability Planning

- Database indexing for trend queries
- CDN for static assets and caching
- Background job queues for data processing
- Monitoring for performance bottlenecks

---

**Note**: This project is in early development. Always check `Checklist.md` for the most current development priorities and feature status.
