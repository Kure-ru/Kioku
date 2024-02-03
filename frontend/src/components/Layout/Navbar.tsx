import {
  Button,
  Link,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Navbar as NextUiNavbar,
} from "@nextui-org/react";

const Navbar = () => {
  return (
    <NextUiNavbar>
      <NavbarBrand>
        <span className="font-bold text-xl ">KIOKU</span>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem className="hidden lg:flex">
          <Link href="#">Login</Link>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} color="primary" href="#" variant="flat">
            Sign Up
          </Button>
        </NavbarItem>
      </NavbarContent>
    </NextUiNavbar>
  );
};

export default Navbar;
