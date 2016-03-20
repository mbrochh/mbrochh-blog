Date: 2016-03-20
Title: TypeError: CSS2Properties doesn't have an indexed property setter for '0'
Tagline: Beware of this nasty pitfall if you use Radium
Slug: react-styles-issue
Category: Blog
Tags: javascript, reactjs

Last Friday it came to my attention that our shop grid on [luxglove.com](https://luxglove.com/products/artworks/) didn't work on Firefox.

When opening the developer tools, I could see this error:

```
TypeError: CSS2Properties doesn't have an indexed property setter for '0'
```

And after a few seconds another error would show up:

```
Error: findComponentRoot(...):

Unable to find element. This probably means the DOM was unexpectedly
mutated (e.g., by the browser), usually due to forgetting a <tbody>
when using tables, nesting tags like <form>, <p>, or <a>, or using
non-SVG elements in an <svg> parent. Try inspecting the child nodes
of the element with React ID.
```

I spent five hours trying to find a solution. Mainly because I concentrated
on the bigger, more scary looking error instead of just focusing on the first
one.

What finally led me to the solution was enabling "Pause on Exception" in the
Firefox developer tools. Now I could see that the error happens within the
ReactJS codebase right here:

```javascript
if (styleValue) {
  style[styleName] = styleValue;
} else {
```

By hovering over the variables, I could see that `styleName` was `undefined`
and `styleValue` as an Object.

In the "Variables" panel I could expand the `styles` member and see that it
contained a style `height: "1em"`. Ah-ha! That's something I can search for
in my codebase.

It lead me to a component that contained this:

```
<div className="visible-xs" style={[{height: "1em"}]}>&nbsp;</div>
```

That looked about right to me. I'm doing this all the time. Then it hit me:

This component does not use any other styles. Only this one instance where I
defined the style right there in the `render()` method. Usually I have a
`const styles = {}` variable at the top of my file. In this case, I had not and
when I did a bit of code cleanup I thought:

"Oh, this component doesn't define any styles, so I can remove the Radium
import and the Radium decorator".

Boy was I wrong. Without Radium, `style={[{height: "1em"}]}` is no longer valid
syntax to add styles in vanilla-React.

If you ever face this error and if you use Radium, I hope I might have saved
you a few hours of frustration (and I'm sure my future self will thank me
because I'm pretty sure I'll mess this up at least one more time in my life).
