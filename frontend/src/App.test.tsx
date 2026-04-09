import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders the application title', () => {
    render(<App />)
    expect(screen.getByText('Salary Management')).toBeInTheDocument()
  })

  it('shows a welcome message for the HR manager', () => {
    render(<App />)
    expect(screen.getByText('Welcome, HR Manager')).toBeInTheDocument()
  })
})
