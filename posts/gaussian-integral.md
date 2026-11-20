---
title: The Gaussian Integral: A Beautiful Application of Double Integrals and Polar Coordinates
date: 2026-11-19
tags: Mathematics
summary: How squaring the Gaussian integral turns it into a double integral that polar coordinates can solve.
---
One of the most famous integrals in mathematics is the Gaussian integral:

![I equals the integral from minus infinity to infinity of e to the power minus x squared, dx](images/gaussian-1.png){eq w=209}

Although it looks relatively simple, this integral can’t be evaluated using elementary integration techniques we learn in middle/high school. Surprisingly, after learning Calculus III I found that we can solve it by extending the problem into two dimensions and using polar coordinates.

## 1. A quick introduction to double integrals

A single integral adds up quantities along a one-dimensional interval. A double integral extends this idea to a two-dimensional region.

For example, consider a surface described by the function **z = f (x , y)**. The double integral of this function over a region **D** represents the volume beneath the surface and above that region.

We write this as:

![The double integral over D of f(x, y) dA](images/gaussian-2.png){eq w=161}

Here, **dA** represents a tiny element of area. In Cartesian coordinates, we can write:

![dA = dx dy](images/gaussian-3.png){eq w=145}

One advantage of double integrals is that we can change our coordinate system to simplify the calculation. For circular regions, polar coordinates are particularly useful.

## 2. Changing coordinates: The Jacobian determinant

In Cartesian coordinates, a point is described by its horizontal and vertical coordinates, **x** and **y**.

In polar coordinates, we instead describe the point using its distance from the origin, **r**, and its angle, **θ**.

![Handwritten notes on changing variables in a double integral: a map T from a region D* to a region D, the matrix DT, the Jacobian determinant, and the change of variables theorem](images/gaussian-4.png){eq}

The transformation is:

![x = r cos θ](images/gaussian-5.png){eq w=125}

![y = r sin θ](images/gaussian-6.png){eq w=121}

But changing coordinates also changes how we measure area. In particular, the area element is no longer simply **dr dθ**.

To understand why, we use the **Jacobian determinant**.

The Jacobian matrix is formed by taking the partial derivatives of **x** and **y** with respect to **r** and **θ**:

![J = a 2 by 2 matrix with first row cos θ and minus r sin θ, and second row sin θ and r cos θ](images/gaussian-7.png){eq w=275}

Its determinant is:

![det(J) = r cos² θ + r sin² θ = r(cos² θ + sin² θ) = r](images/gaussian-8.png){eq w=282}

Therefore, the area element becomes:

![dA = r dr dθ](images/gaussian-9.png){eq w=145}

The factor **r** accounts for the stretching of area when we transform from Cartesian coordinates to polar coordinates.

## 3. Evaluate a double integral over a disk

Now, consider a disk centered at the origin with radius **a**. We want to evaluate:

![The double integral over D_a of e to the power minus (x² + y²), dA](images/gaussian-10.png){eq w=184}

Using polar coordinates, we know that:

![x² + y² = r²](images/gaussian-11.png){eq w=157}

and

![dA = r dr dθ](images/gaussian-12.png){eq w=152}

Since we are integrating over a complete disk, our bounds are:

- **r** goes from 0 to a
- **θ** goes from 0 to 2π

![The double integral over D_a equals the integral from 0 to 2π of the integral from 0 to a of e^(−r²) r dr dθ, which works out to π(1 − e^(−a²))](images/gaussian-13.png){eq w=245}

## 4. Let the radius approach infinity

As **a** approaches infinity, our disk expands to cover the entire plane.

Since **e^(-a^2)** approaches zero, we obtain:

![The double integral over the plane of e^(−(x²+y²)) dA equals the limit as a approaches infinity of π(1 − e^(−a²)), which equals π](images/gaussian-14.png){eq w=419}

We have now evaluated the double integral over the entire plane!

## 5. Connect it back to the original integral

Remember that our original goal was to evaluate:

![I equals the integral from minus infinity to infinity of e to the power minus x squared, dx](images/gaussian-15.png){eq w=196}

The trick is to square this integral:

![I squared equals the integral of e^(−x²) dx times the integral of e^(−y²) dy, both from minus infinity to infinity](images/gaussian-16.png){eq w=318}

We introduce a second variable, **y**, because we are now working with a double integral.

Combining the two integrals gives:

![I squared equals the double integral over the plane of e^(−(x²+y²)) dA](images/gaussian-17.png){eq w=275}

But from our calculation using polar coordinates, we already know that this double integral equals π.

Therefore:

![I squared = π](images/gaussian-18.png){eq w=82}

Taking the positive square root, since the integrand is always positive:

![The integral from minus infinity to infinity of e^(−x²) dx equals the square root of π](images/gaussian-19.png){eq w=216}

## 6. Summary

The original one-dimensional integral is difficult to evaluate directly. However, by squaring it, transforming it into a double integral, and switching to polar coordinates, we can take advantage of the radial symmetry of the function.

This problem demonstrates three important mathematical ideas:

**(1) Double integrals:** Extending integration from one dimension to two.

**(2) The Jacobian determinant:** Accounting for changes in area when transforming coordinates.

**(3) Polar coordinates:** Exploiting symmetry to simplify complicated integrals.

Sometimes, the key to solving a difficult mathematical problem is not finding a more complicated technique, but looking at it from a different dimension.

## 7. Extension

In A-level Further Statistics, I encountered the probability density function (PDF) for normal distribution:

![f(x) = 1 over σ√(2π), times e to the power minus (x − μ)² over 2σ²](images/gaussian-20.png){eq w=228}

In probability, a PDF must satisfy one fundamental condition:

![The integral from minus infinity to infinity of f(x) dx equals 1](images/gaussian-21.png){eq w=167}

Back then, I couldn't verify if the total area under the probability density curve for normal distribution equals 1. Now, after knowing about double integration, I'm able to integrate that PDF. How exciting this is!

There are more ways to compute the Gaussian integral, such as using gamma function, fourier transformation, complex analysis, and Feynman's trick. I'm absolutely thrilled to explore and share more about these methods in the future.
