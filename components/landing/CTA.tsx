'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight } from 'lucide-react'

export default function CTA() {
  return (
    <section className="py-20 sm:py-32 bg-background">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl lg:text-5xl">
            Schedule a call and find out how many investor matches we can generate for you
          </h2>
          
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/chat">
              <Button size="lg" className="group h-14 px-8 text-lg font-semibold bg-primary text-primary-foreground hover:bg-primary/90">
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
                className="h-14 border-2 border-foreground px-8 text-lg font-semibold text-foreground hover:bg-foreground hover:text-background"
              >
                Schedule a Call
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
