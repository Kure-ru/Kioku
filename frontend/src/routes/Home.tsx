import { Spacer, Divider, Link, Input, Button } from "@nextui-org/react";

const Home = () => {
  return (
    <div className="min-w-3xl">
      <h2 className="text-xl pb-4">Dashboard</h2>
      <Spacer y={4}></Spacer>
      <ul className="flex flex-row justify-between px-6">
        <li>
          <Link>Deck 1</Link>
        </li>
        <li>
          <Link> Deck 2</Link>
        </li>
        <li>
          <Link> Deck 3</Link>
        </li>
      </ul>
      <Spacer y={4}></Spacer>
      <Divider />
      <div className="flex w-8/12 flex-wrap md:flex-nowrap gap-4">
        <Input
          className="max-w-12"
          type="text"
          label="create a new deck"
          minLength={3}
        />
        <Button type="submit" color="primary">
          add
        </Button>
      </div>
    </div>
  );
};

export default Home;
