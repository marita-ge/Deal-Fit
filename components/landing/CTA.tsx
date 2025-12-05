'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Calendar } from 'lucide-react'

interface CalendlyButtonProps {
  url?: string
}

function CalendlyButton({ url }: CalendlyButtonProps) {
  const calendlyUrl = url || process.env.NEXT_PUBLIC_CALENDLY_URL

  if (!calendlyUrl) {
    return null
  }

  return (
    <a
      href={calendlyUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex"
    >
      <Button variant="outline" size="lg" className="group">
        <Calendar className="mr-2 h-4 w-4" />
        Schedule a Demo
        <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
      </Button>
    </a>
  )
}

export default function CTA() {
  return (
    <section className="py-20 sm:py-32 bg-primary text-primary-foreground">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Ready to Find Your Perfect Investor Match?
          </h2>
          <p className="mt-6 text-lg leading-8 opacity-90">
            Join startups using AI to connect with the right investors. Upload your pitch deck
            and get personalized recommendations in minutes.
          </p>
          
          <div className="mt-10 flex items-center justify-center gap-x-6 flex-wrap gap-y-4">
            <Link href="/chat">
              <Button size="lg" variant="secondary" className="group">
                Get Started Free
                <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <CalendlyButton />
          </div>
        </div>
      </div>
    </section>
  )
}
