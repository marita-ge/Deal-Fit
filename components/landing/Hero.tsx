'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-background py-16 sm:py-24 lg:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="text-5xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl xl:text-8xl">
            Find Your Perfect
            <span className="block">Investor Match</span>
            <span className="block text-primary">in Minutes. Seriously.</span>
          </h1>
          
          <p className="mt-8 text-xl leading-8 text-muted-foreground sm:text-2xl lg:text-3xl">
            We match your pitch deck with the most relevant investors.
          </p>
          <p className="mt-4 text-xl leading-8 text-muted-foreground sm:text-2xl lg:text-3xl">
            We match your pitch deck with the most relevant investors.
          </p>
          <p className="mt-4 text-xl leading-8 text-muted-foreground sm:text-2xl lg:text-3xl">
            We match your pitch deck with the most relevant investors.
          </p>
          
          <div className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/chat">
              <Button size="lg" className="group h-14 px-8 text-lg font-semibold">
                Get Started Free
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
                className="h-14 border-2 border-foreground px-8 text-lg font-semibold hover:bg-foreground hover:text-background"
              >
                Schedule a Call
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </a>
          </div>
          
          <div className="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-3">
            <div className="text-center">
              <div className="text-4xl font-bold text-foreground sm:text-5xl lg:text-6xl">725+</div>
              <div className="mt-2 text-lg text-muted-foreground">Relevant Investors</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-foreground sm:text-5xl lg:text-6xl">AI-Powered</div>
              <div className="mt-2 text-lg text-muted-foreground">Smart Matching</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-foreground sm:text-5xl lg:text-6xl">Direct</div>
              <div className="mt-2 text-lg text-muted-foreground">Contact Info</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
