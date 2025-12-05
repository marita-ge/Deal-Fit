'use client'

import { Card, CardContent } from '@/components/ui/card'

const testimonials = [
  {
    name: 'Sarah Chen',
    company: 'TechFlow, Seed Stage',
    quote: 'Found 15 perfect investor matches in one week. The AI understood our fintech niche better than I expected.',
  },
  {
    name: 'Michael Rodriguez',
    company: 'DataSync, Series A',
    quote: 'Saved me weeks of research. Got 20 targeted matches with direct emails instead of cold outreach.',
  },
  {
    name: 'Emily Johnson',
    company: 'GreenTech, Pre-Seed',
    quote: 'The matching was incredibly accurate. We closed our round with an investor Deal Fit recommended.',
  },
  {
    name: 'David Kim',
    company: 'HealthAI, Seed Stage',
    quote: 'Discovered investors I never would have found. The platform understood our niche market perfectly.',
  },
]

export default function Testimonials() {
  return (
    <section className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl mb-4">
            Loved by Founders
          </h2>
          <p className="text-lg text-muted-foreground">
            See how Deal Fit is helping startups find the right investors
          </p>
        </div>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 max-w-4xl mx-auto">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="border-2 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <p className="text-foreground mb-4 leading-7 text-base">
                  "{testimonial.quote}"
                </p>
                <div className="border-t border-border pt-4">
                  <div className="font-semibold text-foreground">{testimonial.name}</div>
                  <div className="text-sm text-muted-foreground">{testimonial.company}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
