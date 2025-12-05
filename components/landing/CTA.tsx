'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight } from 'lucide-react'

export default function CTA() {
  return (
    <section className="py-20 sm:py-32 bg-gradient-to-b from-muted/30 to-background">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl mb-4">
            Ready to Find Your Perfect Investor Match?
          </h2>
          <p className="text-lg text-muted-foreground mb-10">
            Join startups using AI to connect with the right investors. Get started in minutes.
          </p>
          
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/chat">
              <Button size="lg" className="group h-12 px-8 text-base font-semibold bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg shadow-primary/25">
                Start Matching Now
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <a
              href="https://calendly.com/marita_ge/30min"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button 
                size="lg" 
                variant="outline" 
                className="h-12 border-2 border-border bg-background px-8 text-base font-semibold hover:bg-accent hover:border-primary/50"
              >
                Schedule Demo
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
