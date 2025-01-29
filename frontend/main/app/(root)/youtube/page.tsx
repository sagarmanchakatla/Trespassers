"use client";

import React, { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, ThumbsUp, MessageSquare, Eye } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const YouTubeStats = () => {
  const [channelName, setChannelName] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat("en-US").format(num);
  };

  const fetchChannelStats = async () => {
    if (!channelName.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        // `http://localhost:5001/api/youtube/${encodeURIComponent(channelName)}`
        `http://127.0.0.1:5001/api/youtube/${encodeURIComponent(channelName)}`
      );
      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.statusText}`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const VideoTable = ({ videos, metric }) => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Title</TableHead>
          <TableHead className="w-[100px]">Date</TableHead>
          <TableHead className="text-right">Views</TableHead>
          <TableHead className="text-right">Likes</TableHead>
          <TableHead className="text-right">Comments</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {videos.map((video) => (
          <TableRow key={video.id}>
            <TableCell className="font-medium">{video.snippet.title}</TableCell>
            <TableCell>{formatDate(video.snippet.publishedAt)}</TableCell>
            <TableCell className="text-right">
              {formatNumber(video.statistics.viewCount)}
            </TableCell>
            <TableCell className="text-right">
              {formatNumber(video.statistics.likeCount)}
            </TableCell>
            <TableCell className="text-right">
              {formatNumber(video.statistics.commentCount)}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );

  return (
    <div className="container mx-auto py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>YouTube Channel Statistics</CardTitle>
          <CardDescription>
            Enter a YouTube channel name to view their most popular videos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Input
              placeholder="Enter channel name..."
              value={channelName}
              onChange={(e) => setChannelName(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && fetchChannelStats()}
            />
            <Button
              onClick={fetchChannelStats}
              disabled={loading}
              className="w-32"
            >
              {loading ? (
                <span className="animate-spin">⏳</span>
              ) : (
                <>
                  <Search className="mr-2 h-4 w-4" />
                  Search
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {error && (
        <Card className="mb-8 border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-600">{error}</p>
          </CardContent>
        </Card>
      )}

      {data && (
        <Tabs defaultValue="most_liked" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="most_liked">
              <ThumbsUp className="mr-2 h-4 w-4" />
              Most Liked
            </TabsTrigger>
            <TabsTrigger value="least_liked">
              <ThumbsUp className="mr-2 h-4 w-4" />
              Least Liked
            </TabsTrigger>
            <TabsTrigger value="most_commented">
              <MessageSquare className="mr-2 h-4 w-4" />
              Most Commented
            </TabsTrigger>
            <TabsTrigger value="least_commented">
              <MessageSquare className="mr-2 h-4 w-4" />
              Least Commented
            </TabsTrigger>
          </TabsList>

          <TabsContent value="most_liked">
            <Card>
              <CardHeader>
                <CardTitle>Most Liked Videos</CardTitle>
                <CardDescription>Top videos by like count</CardDescription>
              </CardHeader>
              <CardContent>
                <VideoTable
                  videos={data.video_stats.most_liked}
                  metric="likes"
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="least_liked">
            <Card>
              <CardHeader>
                <CardTitle>Least Liked Videos</CardTitle>
                <CardDescription>Videos with fewest likes</CardDescription>
              </CardHeader>
              <CardContent>
                <VideoTable
                  videos={data.video_stats.least_liked}
                  metric="likes"
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="most_commented">
            <Card>
              <CardHeader>
                <CardTitle>Most Commented Videos</CardTitle>
                <CardDescription>Top videos by comment count</CardDescription>
              </CardHeader>
              <CardContent>
                <VideoTable
                  videos={data.video_stats.most_commented}
                  metric="comments"
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="least_commented">
            <Card>
              <CardHeader>
                <CardTitle>Least Commented Videos</CardTitle>
                <CardDescription>Videos with fewest comments</CardDescription>
              </CardHeader>
              <CardContent>
                <VideoTable
                  videos={data.video_stats.least_commented}
                  metric="comments"
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
};

export default YouTubeStats;
