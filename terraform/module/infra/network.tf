resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

locals {
  az = tolist(["a","c"])
  private = {
    a = "10.0.0.0/24", 
    c = "10.0.1.0/24"
  }
  public = {
    a = "10.0.2.0/24", 
    c = "10.0.3.0/24"
  }
}

resource "aws_subnet" "public_subnet" {
  for_each = local.public
  vpc_id     = aws_vpc.vpc.id
  cidr_block = each.value
  availability_zone = "${var.region}${each.key}"
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  for_each = local.private
  vpc_id     = aws_vpc.vpc.id
  cidr_block = each.value
  availability_zone = "${var.region}${each.key}"
  tags = {
    Name = "${var.project_name}-subnet"
  }
}

resource "aws_route_table" "private_rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block           = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway.id
  }

  tags = {
    Name = "${var.project_name}-rtb"
  }
}

resource "aws_route_table" "public_rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block           = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
  tags = {
    Name = "${var.project_name}-rtb"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table_association" "private_rtba" {
  for_each = aws_subnet.private_subnet
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private_rtb.id
}

resource "aws_route_table_association" "public_rtba" {
  for_each = aws_subnet.public_subnet
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public_rtb.id
}



resource "aws_eip" "eip" {
  domain   = "vpc"
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.eip.id
  subnet_id     =   [
    for k, v in aws_subnet.public_subnet : v.id
  ][0]

  tags = {
    Name = "${var.project_name}-nat"
  }
}
