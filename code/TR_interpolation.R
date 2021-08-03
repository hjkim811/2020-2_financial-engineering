# data
x <- c(1, 2, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360)
y <- c(0.09, 0.09, 0.09, 0.11, 0.13, 0.16, 0.20, 0.38, 0.63, 0.87, 1.41, 1.63)
dat <- data.frame(x, y)

x_s <- c(1, 2, 3, 6, 12, 24)
y_s <- c(0.09, 0.09, 0.09, 0.11, 0.13, 0.16)
dat_s <- data.frame(x_s, y_s)

value <- c(3, 6, 9, 12, 15, 18, 21, 24)

# Linear interpolation
fun1 <- approxfun(x, y, method = "linear")
plot(dat, xlab="Month", ylab="Treasury Rate")
curve(fun1, add=TRUE)
approx(x, y, value, method = "linear")

# Linear interpolation - short ver.
fun1s <- approxfun(x_s, y_s, method = "linear")
plot(dat_s, xlab="Month", ylab="Treasury Rate")
curve(fun1s, add=TRUE)
approx(x_s, y_s, value, method = "linear")


# Spline interpolation - fmm
fun2 <- splinefun(x, y, method="fmm")
plot(dat, xlab="Month", ylab="Treasury Rate")
curve(fun2, add=TRUE)
spline(x, y, method = "fmm", xout=value)


# Spline interpolation - natural
fun3 <- splinefun(x, y, method="natural")
plot(dat, xlab="Month", ylab="Treasury Rate")
curve(fun3, add=TRUE)
spline(x, y, method = "natural", xout=value)

# Spline interpolation - natural - short ver.
fun3s <- splinefun(x_s, y_s, method="natural")
plot(dat_s, xlab="Month", ylab="Treasury Rate")
curve(fun3s, add=TRUE)
spline(x_s, y_s, method = "natural", xout=value)

# Spline interpolation - hyman
fun4 <- splinefun(x, y, method="hyman")
plot(dat, xlab="Month", ylab="Treasury Rate")
curve(fun4, add=TRUE)
spline(x, y, method = "hyman", xout=value)

# Spline interpolation - default
fun5 <- splinefun(x, y)
plot(dat, xlab="Month", ylab="Treasury Rate")
curve(fun5, add=TRUE)
spline(x, y, xout=value)
# default, fmm, hyman 결과 같게 나옴


# Lagrangian polynomial interpolation - 실패
library(polynom)
library(ggplot2)

x <- c(0, 2, 3, 4)
y <- c(7, 11, 28, 63)

dat <- data.frame(cbind(x, y))

poly.calc(x, y)


f <- function(x) {
  return( 7 - 2*x + x^3  )
}


ggplot(dat, aes(x=x, y=y)) + 
  geom_point(size=5, col='blue') + 
  stat_function(fun = f, size=1.25, alpha=0.4)

