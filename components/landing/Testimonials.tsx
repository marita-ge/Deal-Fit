'use client'

import { Card, CardContent } from '@/components/ui/card'

const testimonials = [
  {
    name: 'Sarah Chen',
    company: 'TechFlow, Seed',
    quote: 'Deal Fit helped me find 15 highly relevant investors in just one week. The AI matching was incredibly accurate, and I had meetings scheduled within days.',
  },
  {
    name: 'Michael Rodriguez',
    company: 'DataSync, Series A',
    quote: 'I was skeptical at first, but Deal Fit\'s recommendations were spot-on. We closed our Series A with an investor they matched us with. Game changer.',
  },
  {
    name: 'Emily Johnson',
    company: 'GreenTech, Pre-Seed',
    quote: 'The platform saved me weeks of research. Instead of cold emailing hundreds of investors, I got 20 targeted matches with direct contact information.',
  },
  {
    name: 'David Kim',
    company: 'HealthAI, Seed',
    quote: 'Deal Fit expanded my investor network beyond expectations. The AI understood our niche market and found investors I never would have discovered.',
  },
  {
    name: 'Lisa Wang',
    company: 'FinTech Solutions, Series A',
    quote: 'Most effective tool I\'ve used for fundraising. Investors showed up knowing our deck and ready to talk. Highly recommend.',
  },
  {
    name: 'James Thompson',
    company: 'CloudScale, Seed',
    quote: 'We got 30 investor introductions in 2 months through Deal Fit. The quality of matches was exceptional, and the process was seamless.',
  },
]

export default function Testimonials() {
  return (
    <section className="py-20 sm:py-32 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl lg:text-5xl">
            Trusted by Founders
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Real founders saying about us
          </p>
        </div>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="border-2 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <p className="text-foreground mb-4 leading-7">
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
